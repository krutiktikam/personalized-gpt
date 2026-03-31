# Aura AI Companion 🤖

A personalized AI assistant with emotion awareness and conversation memory.

## Features
- **Emotion Recognition**: Analyzes user sentiment to tailor responses.
- **Persistent Memory**: Remembers past interactions using SQLite.
- **Modular Pipeline**: Decoupled GPT, emotion, and personality modules.
- **FastAPI Backend**: Scalable API for web/mobile integration.

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Set your Hugging Face token in a `.env` file: `HUGGINGFACE_TOKEN=your_token_here`
3. Run the API: `python -m src.api.app`