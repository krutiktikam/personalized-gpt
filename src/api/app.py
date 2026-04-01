from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.gpt.pipeline import run_pipeline
import uvicorn
import sys
from pathlib import Path

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.settings import settings
from src.utils.logger import logger
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title=settings.APP_NAME)

# --- ADD THIS BLOCK TO FIX THE 405 ERROR ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your HTML file to connect
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, OPTIONS, etc.
    allow_headers=["*"],
)
# --------------------------------------------

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error occurred: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"error": True, "message": "Invalid request body", "details": exc.errors()},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": "An internal server error occurred"},
    )

class ChatRequest(BaseModel):
    message: str
    mode: str = "default"

@app.get("/", summary="Check if Aura AI is online")
def home():
    return {"status": "Aura AI is online"}

@app.get("/memory", summary="Get user facts from long-term memory")
async def get_memory(category: str = None):
    try:
        from src.utils.memory import memory
        return memory.get_preferences(category=category)
    except Exception as e:
        logger.error(f"Error in memory endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/memory/clear", summary="Clear all stored user facts")
async def clear_memory():
    try:
        from src.utils.memory import memory
        memory.clear_preferences()
        return {"status": "success", "message": "Memory cleared"}
    except Exception as e:
        logger.error(f"Error clearing memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", summary="Send a message to Aura AI")
async def chat(request: ChatRequest):
    try:
        # Call the pipeline (returns a dict now)
        pipeline_output = run_pipeline(request.message, mode=request.mode)

        return {
            "reply": pipeline_output["reply"],
            "emotion": pipeline_output["emotion"],
            "mode_used": request.mode
        }
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info(f"🚀 {settings.APP_NAME} API starting on http://{settings.API_HOST}:{settings.API_PORT}")
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)