# 🤖 InsightBot — AI Research Assistant

> A Streamlit-powered research assistant that combines **RAG (Retrieval-Augmented Generation)**, **live web search**, and **Groq LLM** to answer your questions intelligently.

---

## ✨ Features

| Feature | Details |
|---|---|
| 💬 **AI Chat** | Powered by Groq's `llama-3.1-8b-instant` via LangChain |
| 📄 **Chat with PDF** | Upload any PDF — the bot reads and answers from it using RAG |
| 🌐 **Live Web Search** | Toggle Tavily search for real-time information |
| ⚡ **Response Modes** | Switch between **Concise** (2–3 sentences) and **Detailed** answers |
| 🧠 **Local Embeddings** | Uses HuggingFace `all-MiniLM-L6-v2` — no extra API key needed |

---

## 🏗️ Architecture

```
InsightBot/
├── app.py                  ← Main Streamlit app (chat UI, RAG pipeline, web search)
├── requirements.txt        ← Python dependencies
├── .env                    ← API keys (never commit this!)
├── .env.example            ← Template for environment variables
├── config/
│   └── config.py           ← Centralized config (API keys, model names, chunk settings)
├── models/
│   ├── llm.py              ← Groq chat model wrapper (llama-3.1-8b-instant)
│   └── embeddings.py       ← HuggingFace embedding model wrapper
└── utils/
    ├── rag.py              ← PDF loader, text splitter, FAISS vectorstore, retrieval
    └── web_search.py       ← Tavily live web search integration
```

**Data Flow:**
```
User Query
    │
    ├─► [PDF Uploaded?] → RAG retrieval (FAISS) → context chunks
    │
    ├─► [Web Search ON?] → Tavily search → live web results
    │
    └─► Groq LLM (llama-3.1-8b-instant) + context → Final Answer
```

---

## 🔑 Prerequisites

- **Python 3.9+**
- API keys from:
  - [Groq Console](https://console.groq.com/keys) — for the LLM
  - [Tavily](https://app.tavily.com) — for live web search

---

## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/PriyanshuRanjan04/InsightBot.git
cd InsightBot
```

### 2. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** The first run will download the HuggingFace embedding model (~90 MB). This happens automatically and only once.

### 4. Configure Environment Variables

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GOOGLE_API_KEY=your_google_api_key_here   # optional, not used for embeddings
```

#### Where to get API keys:

| Service | URL | Purpose |
|---|---|---|
| Groq | [console.groq.com/keys](https://console.groq.com/keys) | LLM chat model |
| Tavily | [app.tavily.com](https://app.tavily.com) | Live web search |

### 5. Run the App

```bash
streamlit run app.py
```

Or if `streamlit` is not on your PATH:

```bash
python -m streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

---

## 🚀 Hosting Options

### Option 1 — Streamlit Community Cloud *(Recommended, Free)*

The easiest way to share InsightBot publicly.

1. Push your code to a **public GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **"New app"** and select your repository
4. Set **Main file path** to `app.py`
5. Go to **Advanced settings → Secrets** and add your environment variables:
   ```toml
   GROQ_API_KEY = "your_groq_api_key"
   TAVILY_API_KEY = "your_tavily_api_key"
   ```
6. Click **Deploy** — your app gets a public URL like `https://yourapp.streamlit.app`

> ⚠️ **Never push your `.env` file to GitHub.** Make sure `.env` is in your `.gitignore`.

---

### Option 2 — Railway *(Free tier available)*

1. Sign up at [railway.app](https://railway.app)
2. Click **"New Project" → "Deploy from GitHub repo"**
3. Select your InsightBot repository
4. Under **Variables**, add:
   - `GROQ_API_KEY`
   - `TAVILY_API_KEY`
5. Add a `Procfile` in the root (Railway needs this):
   ```
   web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```
6. Railway auto-detects Python and deploys your app with a public URL.

---

### Option 3 — Render *(Free tier available)*

1. Sign up at [render.com](https://render.com)
2. Click **"New" → "Web Service"** and connect your GitHub repo
3. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port 10000 --server.address 0.0.0.0`
4. Under **Environment**, add your API keys as environment variables
5. Click **Create Web Service**

---

### Option 4 — Docker *(Self-hosted)*

Create a `Dockerfile` in the project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t insightbot .
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_key \
  -e TAVILY_API_KEY=your_key \
  insightbot
```

App is available at **http://localhost:8501**.

---

## 📝 Configuration Reference

All settings live in `config/config.py`:

| Variable | Default | Description |
|---|---|---|
| `GROQ_MODEL` | `llama-3.1-8b-instant` | Groq LLM model name |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace embedding model |
| `CHUNK_SIZE` | `1000` | Characters per document chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `MAX_RETRIEVAL_DOCS` | `3` | Number of chunks retrieved from vectorstore |
| `MAX_SEARCH_RESULTS` | `3` | Number of Tavily web results fetched |

### Available Groq Models

| Model | Speed | Capability |
|---|---|---|
| `llama-3.1-8b-instant` | ⚡ Fast | Good for most tasks |
| `llama-3.1-70b-versatile` | 🐢 Slower | More powerful, detailed answers |
| `mixtral-8x7b-32768` | ⚡ Fast | Good balance, long context |

See all models at [console.groq.com/docs/models](https://console.groq.com/docs/models).

---

## 🛠️ Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `Did not find groq_api_key` | Missing or empty API key | Check `.env` file has `GROQ_API_KEY` set |
| `streamlit: command not found` | Streamlit not on PATH | Use `python -m streamlit run app.py` |
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements.txt` |
| Web search not working | Missing Tavily key | Add `TAVILY_API_KEY` to `.env` |
| Slow first startup | Downloading embedding model | Wait ~30 seconds, happens once only |

---

## 📦 Tech Stack

- **[Streamlit](https://streamlit.io)** — Web UI framework
- **[LangChain](https://python.langchain.com)** — LLM orchestration & RAG pipeline
- **[Groq](https://groq.com)** — Ultra-fast LLM inference
- **[FAISS](https://faiss.ai)** — Vector similarity search
- **[HuggingFace Sentence Transformers](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)** — Local text embeddings
- **[Tavily](https://tavily.com)** — Real-time web search API
- **[PyPDF](https://pypdf.readthedocs.io)** — PDF text extraction

---

## 📄 License

This project is open source. Feel free to fork, modify, and build on top of it.

---

<p align="center">Built with ❤️ using Streamlit + LangChain + Groq</p>
