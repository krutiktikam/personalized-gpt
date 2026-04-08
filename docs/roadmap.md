# Aura AI: Industry-Ready & Portfolio Roadmap 🚀

This schedule transforms Aura from a "working script" into a professional AI product.

## Phase 1: Stability & Best Practices (Week 1)
*Goal: Ensure the code is robust, readable, and professional.*
- [x] Day 1-2: Centralize Configuration. Move all hardcoded values and paths to `config/settings.py` using Pydantic-settings.
- [x] Day 3: Structured Logging. Replace `print()` statements with a proper `logging-module` to track API calls and errors.
- [x] Day 4: Unit Testing. Write tests for `src/emotion/detect.py` and `src/utils/memory.py` using `pytest`.
- [x] Day 5: Error Handling. Implement global FastAPI exception handlers for better API responses.
- [x] GitHub Strategy: Commit daily with descriptive messages.

## Phase 2: Advanced Feature - "The Big Sibling" Memory (Week 2)
*Goal: Implement long-term user recognition.*
- [x] Day 1-2: Database Schema Update. Add a `user_preferences` table to store facts.
- [x] Day 3-4: Fact Extraction. Use the LLM to identify when a user shares a fact and store it.
- [x] Day 5: Contextual Injection. Before generating a reply, query the "Fact File" and inject those facts.
- [x] GitHub Strategy: Commit feature-by-feature.

## Phase 3: Industry Standards & DevOps (Week 3)
*Goal: Show you can deploy and maintain real software.*
- [x] Day 1: Dockerization. Create a `Dockerfile` and `docker-compose.yml` to make Aura run anywhere.
- [x] Day 2: API Documentation. Fully document the `/chat` and `/memory` endpoints using FastAPI's built-in Swagger (OpenAPI).
- [x] Day 3: CI/CD. Set up a GitHub Action to run your tests automatically on every push.
- [x] Day 4: Frontend Polish. Clean up `chat.html` with a modern CSS framework (like Tailwind or a clean custom UI).
- [x] GitHub Strategy: Small, frequent commits for Docker and CI configuration.

## Phase 4: Portfolio Presentation & Future Expansion (Week 4)
*Goal: "Sell" the project and plan the next steps.*
- [x] Day 1-2: README Overhaul. Added architectural diagrams, screenshots, and "Technical Challenges".
- [ ] Day 3: Demo Recording. Record a 2-minute video.
- [x] Day 4: Final Cleanup. Removed leftover debug files.
- [x] Day 5: Mobile Expansion Planning. Created `docs/mobile_expansion.md` for future API development.
- [x] GitHub Strategy: Final "Documentation" and "UI Polish" commits to show attention to detail.

## Phase 5: Intelligence & Context (The "Deep Thinker" Update)
*Goal: Move beyond simple memory to active knowledge retrieval and smarter reasoning.*
- [x] RAG Integration (Retrieval-Augmented Generation): Implemented ChromaDB to store docs and user snippets.
- [x] Code-Review Mode: New personality mode `/review` for security and clean code analysis.
- [x] Architecture Documentation: Created `docs/tech_stack.md` to explain core concepts and library choices.
- [x] Multi-Model Routing: Implemented routing logic in `src/gpt/router.py` to distinguish simple vs complex tasks.
- [x] Tool Use (Function Calling): Implemented `src/gpt/tool_handler.py` with intent-based auto-triggering.

## Phase 6: Professional Infrastructure (The "SaaS-Ready" Update)
*Goal: Prepare the architecture for multiple users and professional monitoring.*
- [ ] JWT Authentication: Secure the FastAPI endpoints with JSON Web Tokens.
- [ ] Database Migration (SQLite -> PostgreSQL): Move to a more robust database.
- [ ] Observability Dashboard: Integrate Prometheus/Grafana or custom dashboard.
- [ ] Async Pipeline: Refactor pipeline to be fully asynchronous.

## Daily Commit Checklist for GitHub "Green Squares":
1. Morning: Pick one small task from the phase.
2. Afternoon: Implement and test locally.
3. Evening: Commit and Push with a clear message.
4. Keep the "Green" streak alive to show consistency to employers!
