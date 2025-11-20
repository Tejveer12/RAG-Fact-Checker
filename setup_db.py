import os
import asyncio
from vector_db_manager import TrustedFactBase


async def setup_db(facts_file="facts.txt"):
    if not os.path.exists(facts_file):
        print(f"File not found: {facts_file}")
        return

    with open(facts_file, "r", encoding="utf-8") as f:
        facts = [line.strip() for line in f if line.strip()]

    if not facts:
        print("No facts found in the file.")
        return

    store = TrustedFactBase()
    await store.add_facts(facts)
    print("Database setup complete!")


if __name__ == "__main__":
    asyncio.run(setup_db())
