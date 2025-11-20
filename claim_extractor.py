import os

import aiohttp
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from parameters import *

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class ClaimExtractor:
    def __init__(self):
        self.gemini_api_key = GOOGLE_API_KEY
        self.local_api_url = LOCAL_API_URL
        self.local_model = LOCAL_MODEL

    async def extract_claim(self, text: str):
        return await self._call_local_llm(text)


    async def _call_local_llm(self, text: str):
        system_prompt = """
You are an AI that extracts factual claims concisely.
Return JSON only:
{
  "claim": "...",
  "entities": ["..."],
  "summary": "..."
}
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]

        payload = {
            "model": self.local_model,
            "messages": messages,
            "max_tokens": 256,
            "temperature": 0.2,
            "top_p": 0.95,
            "stop": ["</s>"],
            "stream": False
        }

        headers = {"Content-Type": "application/json", "accept": "application/json"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.local_api_url, headers=headers, json=payload, timeout=60) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = data["choices"][0]["message"].get("content", "").strip()
                        return content
                    else:
                        return await self._fallback_gemini(text)

        except Exception:
            return await self._fallback_gemini(text)

    async def _fallback_gemini(self, text: str):
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=self.gemini_api_key,
                temperature=0.2,
            )

            prompt = ChatPromptTemplate.from_messages([
                ("system",
                 """Extract factual claim + entities. Return JSON only:
    {{
      "claim": "...",
      "entities": ["..."],
      "summary": "..."
    }}"""),
                ("user", "{text}")
            ])

            messages = prompt.format_messages(text=text)

            response = await llm.ainvoke(messages)

            return response.content.strip()
        except Exception as e:
            raise e

