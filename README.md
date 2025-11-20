# 🧐 RAG Fact Checker

A **fact-checking web app** that verifies claims against a trusted knowledge base using a retrieval-augmented generation (RAG) approach. Enter any claim or statement, and the system checks it against verified facts and provides a verdict with a confidence score and explanation.

---

## Features

- ✅ Check claims against a trusted fact database.
- 💡 Provides a **verdict**: True, False, or Unverifiable.
- 📊 Shows **confidence score** for the claim.
- 📝 Displays a detailed **reason/explanation** for the verdict.
- ⚡ Simple and intuitive **Streamlit-based GUI**.
- 🗂 Includes a **setup_db script** to initialize the Milvus Lite database with facts.

--

## Installation

1. **Clone the repository:**

```bash
    git clone https://github.com/Tejveer12/RAG-Fact-Checker.git
    cd RAG-Fact-Checker
```

2. **Create and activate a virtual environment:**

```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows
```
3. **Install dependencies:**

```bash
    pip install -r requirements.txt
```

## Vector Database Setup

Before running the app, initialize the Milvus Lite database with trusted facts:

```bash
  python setup_db.py
```

This script will:

- Connect to Milvus Lite. 
- Create a collection for storing facts and embeddings. 
- Add all facts from facts.txt or your preferred fact source.

## Setup .env file or Local Model Configuration
Now, Create a `.env` file add a Google Gemini API Key like below

```bash
  GOOGLE_API_KEY=<YOUR_API_KEY>
```

Or 

If you want to run it with local llm just update `LOCAL_API_URL` and `LOCAL_MODEL` in `parameters.py`
```python
LOCAL_API_URL="http://192.168.12.1:8009/v1/chat/completions"
LOCAL_MODEL="Qwen/Qwen3-4B-Instruct-2507"
```


## Running the App

Start the backend server (FastAPI):
```bash
  uvicorn api:app --host 0.0.0.0 --port 8000
```

Run the Streamlit frontend:

```bash
  streamlit run interface.py
```


Open the URL displayed by Streamlit (usually http://localhost:8501) in your browser.

Enter a claim in the text area and click Check Claim to see the verdict, score, and reason.

