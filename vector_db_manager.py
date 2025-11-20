import os
import uuid
import asyncio
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from sentence_transformers import SentenceTransformer

class TrustedFactBase:
    _lock = asyncio.Lock()

    def __init__(self, db_path="volumes/milvus.db", collection_name="trusted_facts"):
        self.collection_name = collection_name
        directory = os.path.dirname(db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")

        connections.connect(alias="default", uri=db_path)
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self._create_collection()

    def _create_collection(self):
        existing = utility.list_collections()
        if self.collection_name in existing:
            self.collection = Collection(self.collection_name)
        else:
            fields = [
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2048),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
            ]
            schema = CollectionSchema(fields, description="Trusted Fact RAG Store")
            self.collection = Collection(self.collection_name, schema)
            self.collection.create_index(
                field_name="embedding",
                index_params={
                    "index_type": "IVF_FLAT",
                    "metric_type": "L2",
                    "params": {"nlist": 128},
                }
            )

    async def add_facts(self, fact_list):
        async with self._lock:
            embeddings = self.embedder.encode(fact_list).tolist()
            ids = [str(uuid.uuid4()) for _ in fact_list]
            self.collection.insert([ids, fact_list, embeddings])
            self.collection.flush()
            print(f"Inserted {len(fact_list)} facts into Milvus Lite.")

    async def search(self, query_text, k=3):
        async with self._lock:
            query_emb = self.embedder.encode([query_text]).tolist()
            self.collection.load()
            results = self.collection.search(
                data=query_emb,
                anns_field="embedding",
                param={"metric_type": "L2", "params": {"nprobe": 16}},
                limit=k,
                output_fields=["text"],
            )

            hits = []
            for hit in results[0]:
                hits.append({
                    "text": hit.entity.get("text"),
                    "score": float(hit.distance)
                })
            return hits