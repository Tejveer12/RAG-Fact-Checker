from verdict_scorer import VerdictClassifier
from claim_extractor import ClaimExtractor
from vector_db_manager import TrustedFactBase
from utils import extract_claim_json

class RAGFactChecker:
    def __init__(self):
        self.extractor = ClaimExtractor()
        self.retriever = TrustedFactBase()
        self.scorer = VerdictClassifier()

    async def check(self, text):
        try:
            claim_raw_output = await self.extractor.extract_claim(text)

            claim_data = extract_claim_json(claim_raw_output)
            claim = claim_data["claim"]

            facts = await self.retriever.search(claim)

            verdict = await self.scorer.classify(claim, facts)

            return verdict

        except Exception as e:
            raise e