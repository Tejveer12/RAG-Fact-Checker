import aiohttp
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from parameters import *

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


class VerdictClassifier:
    def __init__(self):
        self.gemini_api_key = GOOGLE_API_KEY
        self.local_api_url = LOCAL_API_URL
        self.local_model = LOCAL_MODEL

    async def classify(self, claim: str, retrieved_facts: list):
        return await self._call_local_llm(claim, retrieved_facts)

    async def _call_local_llm(self, claim: str, retrieved_facts: list):
        system_prompt = f"""
You are an expert fact-checking AI.

Compare the user's claim against the retrieved verified facts.

Return STRICT JSON ONLY in this format:
{{
  "verdict": "True | False | Unverifiable",
  "score": 0.0-1.0,
  "reason": "..."
}}

Rules:
- "True" → The claim directly matches or is strongly supported by the facts.
- "False" → The facts directly contradict the claim.
- "Unverifiable" → No reliable match in the retrieved facts.
- Score should represent confidence.
"""

        facts_joined = "\n- ".join(
            f.get("text", "") if isinstance(f, dict) else str(f)
            for f in retrieved_facts
        )

        user_prompt = f"""
Claim: {claim}

Retrieved Facts:
- {facts_joined}
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
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
                        return data["choices"][0]["message"]["content"].strip()
                    else:
                        return await self._fallback_gemini(claim, retrieved_facts)
        except Exception:
            return await self._fallback_gemini(claim, retrieved_facts)

    async def _fallback_gemini(self, claim: str, retrieved_facts: list):
        try:

            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=self.gemini_api_key,
                temperature=0.2,
            )

            facts_joined = "\n- ".join(
                f.get("text", "") if isinstance(f, dict) else str(f)
                for f in retrieved_facts
            )

            system_prompt_text = """You are an expert fact-checking AI.
    Compare the claim with retrieved facts.
    
    Return JSON ONLY in this format:
    {{
      "verdict": "True | False | Unverifiable",
      "score": 0.0-1.0,
      "reason": "..."
    }}"""

            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt_text),
                ("user", "Claim: {claim}\n\nRetrieved Facts:\n- {facts}")
            ])

            messages = prompt.format_messages(
                claim=claim,
                facts=facts_joined
            )

            response = await llm.ainvoke(messages)
            return response.content.strip()

        except Exception as e:
            raise e
