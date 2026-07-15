# FelicityTech — Backend AI Engineering

Portfolio of AI and software engineering projects, built and maintained as a solo developer under the FelicityTech name. Focus areas: full-stack AI application development, applied machine learning, and academic research support — with an emphasis on shipping complete, working, tested systems rather than notebooks or proofs of concept.

---

## About

FelicityTech is a solo AI/software development practice covering:
- End-to-end AI application development (backend pipelines, retrieval systems, agentic tools)
- Applied machine learning and data science (model training, evaluation, competition pipelines)
- Academic research support (thesis statistical modeling, research paper writing and analysis)

Every project in this portfolio is designed, built, and delivered as a complete system — including setup instructions, dependency management, and (where applicable) test coverage.

---

## Core Stack

**AI / LLM**
- Gemini API via the `google-genai` SDK (current SDK, not the legacy client)
- Retrieval-Augmented Generation (RAG) pipelines
- Chroma (vector store)
- sentence-transformers (local embeddings)
- markitdown (document ingestion/conversion)
- CrewAI (multi-agent orchestration)

**Interfaces**
- Gradio
- Streamlit

**ML / Data Science**
- Classical ML (feature engineering, ensembling, cross-validation)
- Deep learning (LSTM, MLP)
- Computer vision (YOLOv4-tiny, custom SORT tracking)
- NLTK / TF-IDF for lightweight NLP

**Engineering practices**
- Deterministic tools for factual/arithmetic tasks instead of relying on LLM computation
- Low temperature settings for factual generation tasks
- Anti-hallucination system prompt design
- Subprocess isolation and automated validation (pytest) for agent-generated code
- Environment: Python (pipenv / pip), Git Bash on Windows (MINGW64)

---

## Selected Projects

### AI Agents & RAG (Gemini API series)
A progressively complex series of agent-based systems, each critically evaluated and improved beyond baseline reference implementations:
- **Multi-Tool AI Agent** — general-purpose agent with tool-calling
- **Multi-Document RAG System** — heading-aware chunking, local embeddings, Chroma vector store, Gradio UI, with streaming, query caching, and exponential backoff for latency optimization
- **Research Paper Analyst** — structured extraction and analysis of academic papers
- **App Builder Agent** — generates and validates code with subprocess isolation and pytest checks
- **Multimodal Explorer** — handles mixed text/image/document input
- **YouTube Notes Generator** — two-stage summarization pipeline
- **Agentic EDA Pipeline** — automated exploratory data analysis
- **CrewAI Agentic RAG** — multi-agent retrieval and reasoning system

### Computer Vision & Audio
- **Object Detection & Tracking** — YOLOv4-tiny with a custom SORT tracker implementation
- **LSTM Music Generation** — sequence modeling for original music generation

### NLP
- **Polyglot** — multilingual translation tool
- **FAQ Chatbot** — NLTK and TF-IDF based retrieval chatbot

### Applied Machine Learning
- **Emission Prediction Pipeline** — competition pipeline with 27 engineered features, four models (including a deep MLP), out-of-fold cross-validation, and Nelder-Mead ensemble weight optimization; achieved well below the target RMSE threshold

### Academic Research Support
- Quantitative thesis support: PLS-SEM-style structural path modeling, PCA-based outer loadings, and reliability/validity metrics for a banking-sector employee performance study
- Research paper support: automated cervical precancerous lesion classification from colposcopy images (clinical dataset), including Discussion and Conclusion sections

---

## Working Principles

- Every deliverable is a complete, runnable system — not a partial script
- Dependencies pinned where breaking changes are known (e.g. `opencv-python<5.0`)
- Vector store collections cleared before re-ingestion to avoid stale data
- Factual/computational logic handled deterministically, not left to LLM inference
- Setup validated in a Windows/Git Bash environment before delivery

---

## Contact

Built and maintained by Eunice (FelicityTech).
