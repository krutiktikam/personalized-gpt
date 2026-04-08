# Aura AI: Technical Stack & Core Concepts

This document explains the "Why" behind the technologies used in Aura, comparing them to industry alternatives.

## 1. Core Brain (LLM)
*   **Model**: Qwen 2.5 (3B-Instruct)
*   **Why**: At 3 billion parameters, it strikes the perfect balance for local execution on mid-range hardware (like an RTX 3050 4GB). It outperforms many 7B models in logic and instruction following while consuming significantly less VRAM.
*   **Alternative**: Llama 3 (8B). While more powerful, it requires at least 6-8GB of VRAM even with heavy quantization, making it less accessible for a "personal" local assistant on this specific hardware.

## 2. API Framework
*   **Library**: FastAPI
*   **Why**: It is natively asynchronous, which is crucial for handling long-running LLM inference without blocking other user requests. It also provides automatic OpenAPI (Swagger) documentation.
*   **Alternative**: Flask. Flask is synchronous and requires more boilerplate for modern API features like data validation.

## 3. Persistent Memory (Relational)
*   **Database**: SQLite
*   **Why**: Serverless and zero-configuration. It's perfect for a personal AI because all data stays in a single `.db` file on your machine.
*   **Alternative**: PostgreSQL. We plan to migrate to Postgres in Phase 6 for professional multi-user support, but SQLite is the fastest path for local development.

## 4. RAG & Knowledge Retrieval (Vector DB)
*   **Library**: ChromaDB
*   **Why**: It is an "AI-native" database that can run completely in-memory or on disk with a single command. It handles the storage and searching of vector embeddings with minimal overhead.
*   **Alternative**: FAISS. FAISS is a powerful library by Meta but lacks the built-in metadata management and persistence features that Chroma provides out-of-the-box.

## 5. Embeddings (The "Senses")
*   **Model**: `all-MiniLM-L6-v2` (via Sentence-Transformers)
*   **Why**: This model is tiny (80MB) and incredibly fast. It transforms text into 384-dimensional vectors that allow Aura to "understand" the meaning of a question rather than just matching keywords.
*   **Alternative**: OpenAI `text-embedding-3-small`. Requires an API key, internet connection, and costs money per request. Our local choice ensures 100% privacy and zero cost.

## 6. Quantization
*   **Library**: BitsAndBytes (4-bit)
*   **Why**: Quantization reduces the precision of model weights from 16-bit to 4-bit. This allows us to fit a 3B model into ~2.5GB of VRAM instead of ~6GB, leaving room for the OS and other tasks.
*   **Alternative**: GGUF (via llama.cpp). Great for CPU inference, but BitsAndBytes is the standard for high-performance GPU inference using HuggingFace.

## 7. Personality Engine
*   **Concept**: System Prompt Injection + Weighted Quirks
*   **Why**: Instead of fine-tuning a model (which is slow and expensive), we use "Prompt Engineering" to inject personality traits into the system message. This allows Aura to change her "mood" instantly based on JSON configurations.
