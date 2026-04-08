from src.utils.logger import logger

def route_task(user_input, mode="default"):
    """
    Decides which model size to use based on task complexity.
    Returns: 'small' (3B) or 'large' (7B+)
    """
    complex_keywords = [
        "architect", "design", "scalable", "optimize", "refactor", 
        "security", "review", "complex", "system", "infrastructure"
    ]
    
    # Force large for specific modes
    if mode in ["architect", "review"]:
        logger.info(f"🧠 Routing to LARGE model due to mode: {mode}")
        return "large"
        
    # Check for complexity in input
    if any(kw in user_input.lower() for kw in complex_keywords) or len(user_input.split()) > 50:
        logger.info("🧠 Routing to LARGE model due to task complexity.")
        return "large"
        
    logger.info("⚡ Routing to SMALL model for quick response.")
    return "small"
