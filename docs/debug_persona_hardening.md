# Debug Plan: Aura Persona Hardening & Logic Sync

## Status Report (2026-04-11) - RESOLVED
The persona hardening issues have been addressed and verified.

1.  **Inject Robotic Headers:** FIXED. Updated `src/gpt/reflection.py` system prompt and added robust filters in `src/personality/response.py`.
2.  **Confuse Context:** FIXED. User input is now stripped of code blocks before being sent to `extract_facts`.
3.  **Override Settings:** VERIFIED. `config/settings.py` hard-override is working, and logs confirm `qwen2.5:1.5b` usage.

---

## 🛠 Phase 1: Environment & Process Isolation
**Goal:** Ensure we are running the EXACT code on disk.

- [x] **Zombie Process Hunt:** Used `taskkill` to ensure clean state.
- [x] **Bytecode Cleanup:** Deleted all `__pycache__` folders.
- [x] **Path Verification:** Local `src/` is being correctly loaded.

## 🛠 Phase 2: Logic & Extraction Debugging
**Goal:** Fix the "Code-as-Schedule" hallucination.

- [x] **Trace `extract_facts`:** Added `logger.info` for RAW EXTRACTION in `src/gpt/extract.py`.
- [x] **Refine Scheduler Trigger:** Modified `src/gpt/pipeline.py` to strip code blocks before extraction.
- [x] **Reflection Logic Audit:** Removed "Autonomous Reflection" label from `src/gpt/reflection.py` and improved `shape_response` filters.

## 🛠 Phase 3: Persona "Kill-Switch"
**Goal:** Force the filters to be absolute.

- [x] **Hard-Filter Injection:** Moved and expanded filters in `src/personality/response.py`'s `shape_response` method.
- [x] **Ollama Version Lock:** Verified available models via API and confirmed settings point to `1.5b`.

---

## ✅ Final Results
- Code snippets no longer trigger the scheduler.
- Reflections are naturally integrated with "Thinking ahead..." and no robotic headers.
- Settings are respected and logged correctly.
