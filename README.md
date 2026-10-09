<div align="center">

<img src="https://img.shields.io/badge/NeuraMed-AI%20Healthcare-00d4aa?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MiA1MiI+PGNpcmNsZSBjeD0iMjYiIGN5PSIyNiIgcj0iMjQiIHN0cm9rZT0iIzAwZDRhYSIgc3Ryb2tlLXdpZHRoPSIxLjUiIGZpbGw9Im5vbmUiLz48cG9seWxpbmUgcG9pbnRzPSI2LDI2IDEyLDI2IDE1LDE2IDE4LDM2IDIyLDIwIDI1LDMwIDI4LDIyIDMxLDMyIDM0LDE4IDM3LDI4IDQwLDI2IDQ2LDI2IiBzdHJva2U9IiMwMGQ0YWEiIHN0cm9rZS13aWR0aD0iMiIgZmlsbD0ibm9uZSIvPjwvc3ZnPg==" alt="NeuraMed Badge" />

# 🧠 NeuraMed
### *Where Intelligence Meets Care*

**An enterprise-grade AI Medical Intelligence Platform powered by Retrieval-Augmented Generation (RAG)**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.27-1C3A5F?style=flat-square)](https://python.langchain.com)
[![Groq](https://img.shields.io/badge/Groq-LPU%20Inference-F54A00?style=flat-square)](https://groq.com)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Store-0064CC?style=flat-square)](https://faiss.ai)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Embeddings-FFD21F?style=flat-square&logo=huggingface&logoColor=black)](https://huggingface.co)

---

</div>

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [How It Works (RAG Pipeline)](#-how-it-works-rag-pipeline)
- [Frontend Design System](#-frontend-design-system)
- [Installation & Setup](#-installation--setup)
- [Environment Configuration](#-environment-configuration)
- [Running the Application](#-running-the-application)
- [Key Features](#-key-features)
- [UI/UX Premium Features](#-uiux-premium-features)
- [Data Flow](#-data-flow)
- [Chunking Strategy](#-chunking-strategy)
- [Built With Love](#-built-with-love)

---

## 🌟 Project Overview

**NeuraMed** is a sophisticated healthcare AI chatbot built using **Retrieval-Augmented Generation (RAG)**. It allows users to ask natural-language medical questions and receive precise, evidence-backed answers drawn from a curated corpus of authoritative medical PDFs.

Unlike generic LLM chatbots, NeuraMed **grounds every response** in real source material — fetching the most relevant passages from a vector database before generating an answer. This dramatically reduces hallucination and increases factual reliability.

### What it does
- Accepts plain-English medical questions via a premium chat interface
- Retrieves the most semantically relevant passages from indexed medical literature
- Feeds the question + retrieved context to a Groq-accelerated LLM
- Returns a precise, readable, evidence-grounded medical answer
- Maintains conversational context across a session

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NeuraMed Architecture                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   User Browser  ──(HTTP POST)──►  Flask App                │
│        ▲                              │                     │
│        │                             ▼                     │
│        │                    RAG Chain (LangChain)          │
│        │                    ┌─────────────────┐            │
│        │                    │  1. Vectorize Q  │            │
│        │                    │  2. FAISS Lookup │            │
│        │                    │  3. Build Prompt │            │
│        │                    │  4. Groq LLM     │            │
│        │                    └────────┬─────────┘            │
│        │                             │                     │
│        └──────(HTML Response)────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Request Lifecycle

```
User Question
    │
    ▼
Flask POST /index
    │
    ▼
Session: Append user message
    │
    ▼
create_qa_chain()
    │
    ├─► Load FAISS VectorStore (from disk)
    │       └─► HuggingFace Embeddings (sentence-transformers)
    │
    ├─► Create Retriever (top-k similar chunks)
    │
    ├─► Load Groq LLM (openai/gpt-oss-120b)
    │
    └─► RetrievalQA.invoke({"query": user_input})
            │
            ▼
        LangChain prompt template + retrieved docs
            │
            ▼
        Groq API → LLM response
            │
            ▼
Session: Append assistant message
    │
    ▼
Render index.html (Jinja2 template)
```

---

## 🛠 Tech Stack

| Category | Technology | Version | Purpose |
|---|---|---|---|
| **Web Framework** | Flask | Latest | HTTP routing, session management, Jinja2 templating |
| **AI Orchestration** | LangChain | 0.3.27 | RAG pipeline, prompt management, chain composition |
| **LLM Community** | langchain-community | 0.3.31 | FAISS vectorstore integrations |
| **LLM Inference** | Groq (via langchain_groq) | 0.3.8 | Ultra-fast LPU-accelerated LLM inference |
| **Embeddings** | HuggingFace (langchain_huggingface) | 0.3.1 | Sentence-transformer embeddings for semantic search |
| **Vector Database** | FAISS-CPU | Latest | High-performance approximate nearest neighbor search |
| **Embedding Model** | sentence-transformers | 5.1.1 | Encoding text into dense vector representations |
| **PDF Processing** | PyPDF | Latest | Loading and parsing medical PDF documents |
| **Environment** | python-dotenv | Latest | Secure API key management via `.env` |
| **Templating** | Jinja2 (via Flask) | Built-in | Server-side HTML rendering with template filters |
| **Frontend** | Vanilla HTML + CSS + JS | N/A | Premium UI with zero framework dependencies |
| **Fonts** | Google Fonts (Inter + Space Grotesk) | CDN | Apple-grade typography |

---

## 📁 Project Structure

```
Healthcare via RAG/
│
├── app/                          # Core application package
│   ├── __init__.py
│   ├── application.py            # Flask app factory, routes, nl2br filter
│   │
│   ├── components/               # AI/ML components
│   │   ├── data_loader.py        # PDF document loading (PyPDF)
│   │   ├── embeddings.py         # HuggingFace embedding model initialization
│   │   ├── llm.py                # Groq LLM initialization
│   │   ├── load_pdf.py           # PDF ingestion & chunking pipeline
│   │   ├── retriever.py          # RAG chain creation (RetrievalQA)
│   │   └── vector_store.py       # FAISS vectorstore build & load
│   │
│   ├── common/                   # Shared utilities
│   │   ├── __init__.py
│   │   ├── custom_exception.py   # Custom exception class
│   │   └── logger.py             # Logging configuration
│   │
│   ├── config/                   # Configuration
│   │   ├── __init__.py
│   │   └── config.py             # Path constants, chunk settings
│   │
│   └── templates/
│       └── index.html            # 🌟 Premium NeuraMed UI (all frontend)
│
├── data/                         # Medical PDF source files (gitignored)
├── vectorstore/                  # FAISS index (db_faiss/) — generated
│   └── db_faiss/
├── logs/                         # Application logs
├── mihu/                         # Python virtual environment
├── medical_book.egg-info/        # Package metadata
│
├── .env                          # API keys (GROQ_API_KEY) — never commit
├── requirements.txt              # Python dependencies
└── setup.py                      # Package setup (setuptools)
```

---

## 🔄 How It Works (RAG Pipeline)

### Step 1: Document Ingestion (One-time Setup)
```python
# load_pdf.py — PDFs are loaded and chunked
PyPDFLoader → RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```
Medical PDFs are parsed and split into overlapping 500-token chunks to preserve context across chunk boundaries.

### Step 2: Vectorization & Indexing
```python
# vector_store.py — Chunks are embedded and stored in FAISS
HuggingFaceEmbeddings(model_name="sentence-transformers/...")
    → FAISS.from_documents(chunks, embedding)
    → saved to vectorstore/db_faiss/
```
Each chunk is encoded into a high-dimensional vector and indexed using FAISS for millisecond similarity search.

### Step 3: Query Embedding
```python
# retriever.py — At inference time
FAISS.load_local("vectorstore/db_faiss", embeddings)
    .as_retriever(search_kwargs={"k": top_k})
```
Your question is encoded using the same embedding model, enabling semantic matching against the stored chunks.

### Step 4: LLM Generation
```python
# llm.py + retriever.py
ChatGroq(model="openai/gpt-oss-120b")
RetrievalQA.from_chain_type(
    llm=groq_llm,
    retriever=faiss_retriever,
    chain_type="stuff"
)
```
The retrieved passages + your question are combined into a prompt and sent to Groq's LPU inference engine for ultra-fast generation.

---

## 🎨 Frontend Design System

The entire frontend is contained in a single **948-line `index.html`** file — a self-contained masterpiece requiring no build tools.

### Color Palette (NeuraMed Signature)
| Token | Value | Use |
|---|---|---|
| `--bg-abyss` | `#04080f` | Primary background (Deep Space Navy) |
| `--bg-deep` | `#070d1a` | Secondary background |
| `--teal` | `#00d4aa` | Primary accent (Bioluminescent Teal) |
| `--violet` | `#7c3aed` | Secondary accent (Cosmic Violet) |
| `--cyan` | `#06b6d4` | Tertiary accent (Neural Cyan) |
| `--text-primary` | `#f0f6ff` | Primary text |
| `--text-secondary` | `rgba(240,246,255,0.6)` | Secondary text |

### Typography
- **Display font**: Space Grotesk (headings, logo, numbers)
- **Body font**: Inter (paragraphs, UI elements)
- **System stack**: `-apple-system, BlinkMacSystemFont, 'SF Pro Display'`
- **Letter spacing**: Apple-grade tight tracking (`-0.03em` to `-0.04em` for headings)

### Design Language
- **Glassmorphism**: `backdrop-filter: blur(24px)` frosted panels
- **Gradient text**: Animated 5-second gradient shimmer on headings
- **Border treatment**: 1px `rgba(255,255,255,0.08)` hairlines
- **Shadows**: Layered multi-stop box shadows for depth

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip
- A Groq API key (free at [console.groq.com](https://console.groq.com))
- Medical PDF files to index

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd "Healthcare via RAG"
```

### 2. Create Virtual Environment
```bash
python -m venv mihu
# Windows
mihu\Scripts\activate
# macOS/Linux
source mihu/bin/activate
```

### 3. Install Dependencies
```bash
pip install -e .
# or directly
pip install -r requirements.txt
```

### 4. Add Medical PDFs
Place your medical PDF files inside the `data/` directory:
```
data/
├── harrison_principles.pdf
├── gray_anatomy.pdf
└── medical_pharmacology.pdf
```

### 5. Build the Vector Store
```bash
python -c "from app.components.load_pdf import ingest_documents; ingest_documents()"
```
This indexes all PDFs into `vectorstore/db_faiss/` — only needs to be done once (or when PDFs change).

---

## ⚙️ Environment Configuration

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### Config Settings (`app/config/config.py`)
```python
GROQ_API_KEY   = os.environ.get("GROQ_API_KEY")
DB_FAISS_PATH  = 'vectorstore/db_faiss'     # Vector index location
DATA_PATH      = 'data/'                     # PDF source directory
CHUNK_SIZE     = 500                         # Tokens per chunk
CHUNK_OVERLAP  = 50                          # Overlap between chunks
```

---

## ▶️ Running the Application

```bash
# Activate virtual environment first
mihu\Scripts\activate     # Windows
source mihu/bin/activate  # macOS/Linux

# Run the Flask app
python -m app.application

# Or using the installed package entry point
python -c "from app.application import app; app.run(debug=True)"
```

The app will be available at: **http://localhost:5000**

### Deploying to Vercel

Import this GitHub repository in the [Vercel dashboard](https://vercel.com/new). Vercel uses `api/index.py` as the Flask serverless function and routes public requests through it.

Add these environment variables in the Vercel project settings before deploying:

```env
GROQ_API_KEY=your_groq_api_key
FLASK_SECRET_KEY=a_long_random_secret
```

Generate a session secret locally with `openssl rand -hex 32`. Do not commit either value. The bundled FAISS index is included with the function; PDF ingestion is not required for deployment.

---

## ✨ Key Features

### AI / Backend Features
| Feature | Implementation |
|---|---|
| RAG (Retrieval-Augmented Generation) | LangChain `RetrievalQA` chain |
| Semantic search | FAISS + HuggingFace embeddings |
| Fast LLM inference | Groq LPU (openai/gpt-oss-120b) |
| PDF ingestion | PyPDF + RecursiveCharacterTextSplitter |
| Session memory | Flask server-side sessions |
| Error handling | Custom exception class + try/catch |
| Structured logging | Python logging module (logs/) |
| Newline rendering | Custom `nl2br` Jinja2 filter |

### Frontend Features
| Feature | Implementation |
|---|---|
| Neural particle canvas | Raw Canvas 2D API — animated node-edge graph |
| Custom magnetic cursor | Lagged RAF animation with hover states |
| DNA loading screen | CSS keyframe animations + progress bar |
| Scroll-reveal animations | IntersectionObserver API |
| Animated stat counters | Cubic ease-out RAF counter animation |
| Feature card glow | CSS custom property mouse tracking |
| Ripple touch effects | Dynamic DOM injection + CSS animation |
| Parallax orbs | mousemove event → CSS transform |
| Auto-resize textarea | scrollHeight measurement |
| Typing indicator | Dynamic DOM + CSS bounce animation |
| Glassmorphism panels | `backdrop-filter: blur()` |
| Gradient shimmer text | CSS `background-clip: text` animation |
| Smooth anchor scroll | `scrollIntoView` + prevented default |
| Keyboard accessibility | ARIA labels, roles, keyboard handlers |
| macOS window chrome | Decorative dot row (red/amber/green) |

---

## 🎭 UI/UX Premium Features

### Hero Sections (6 total)
1. **Hero #1 — Landing** — Full-screen neural particle canvas, animated headline, glow orbs, parallax
2. **Hero #2 — Features** — 6-card glassmorphism feature grid with mouse-tracking glow
3. **Hero #3 — Technology** — Split layout tech pill showcase with spring animations
4. **Hero #4 — Statistics** — Animated counter cards (99%, 500 chunks, etc.)
5. **Hero #5 — How It Works** — Vertical timeline with gradient connector line
6. **Hero #6 — Chat Interface** — Full premium chat UI with typing indicators

### Special Effects
- 🌐 **Neural Canvas**: 80-node animated particle network (WebGL-lite)
- 🖱️ **Magnetic Cursor**: Custom cursor with 0.12 lag coefficient
- 💫 **Ripple Touch**: Bioluminescent tap ripple on all surfaces
- 🔢 **Counter Animation**: Cubic ease-out counter from 0 to target
- 🌊 **Scroll Reveal**: Fade + translate/scale on viewport entry
- ✨ **Gradient Shimmer**: Infinite 5-second gradient cycle on hero text
- 💓 **Heartbeat Footer**: CSS keyframe double-pulse on ❤️ emoji
- 🌙 **Orb Parallax**: Mouse-tracked floating background orbs

---

## 📊 Data Flow

```
User asks: "What are the symptoms of diabetes?"
          │
          ▼
Flask receives POST → session stores user message
          │
          ▼
create_qa_chain() builds:
  ┌── HuggingFaceEmbeddings (all-MiniLM-L6-v2 or similar)
  ├── FAISS.load_local("vectorstore/db_faiss")
  ├── retriever = vectorstore.as_retriever(k=3-5)
    └── ChatGroq(model="openai/gpt-oss-120b")
          │
          ▼
RetrievalQA.invoke({"query": "What are the symptoms of diabetes?"})
  ┌── Embed query → 768-dim vector
  ├── FAISS search → top-k similar chunks (e.g., from medical textbook)
  ├── Build prompt: "[Context: ...retrieved passages...]\nQuestion: ..."
  └── Groq API → LLM generates answer
          │
          ▼
Response stored in Flask session → rendered in index.html
```

---

## 📐 Chunking Strategy

```
Chunk Size: 500 tokens
Overlap:    50 tokens (10% overlap)

Why this matters:
- Too small chunks → lose context within a concept
- Too large chunks → noisy retrieval, irrelevant content mixed in
- 50-token overlap → ensures concepts spanning chunk boundaries are captured
```

---

## 🤝 Contributing

This project follows a clean modular structure — each component has a single responsibility:
- `data_loader.py` — Load PDFs only
- `embeddings.py` — Embedding model only
- `llm.py` — LLM client only
- `vector_store.py` — FAISS operations only
- `retriever.py` — Chain assembly only
- `application.py` — Flask routing only

---

## 📜 License

© 2025–2026 NeuraMed. All rights reserved.

---

<div align="center">

Built with ❤️ by **Mihir**

*NeuraMed — Where Intelligence Meets Care*

</div>
