from fastapi import FastAPI
from pydantic import BaseModel

from rag_pipeline import RAGFactChecker

app = FastAPI(title="RAG Fact Checker API")
checker = RAGFactChecker()

class ClaimRequest(BaseModel):
    text: str

@app.post("/check_claim")
async def check_claim(req: ClaimRequest):
    try:
        verdict = await checker.check(req.text)
        return {"verdict": verdict}
    except Exception as e:
        return {"error": str(e)}
