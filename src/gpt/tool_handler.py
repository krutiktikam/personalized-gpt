import datetime
import os
import json
from src.utils.logger import logger

def get_time():
    """Returns the current time."""
    return f"The current system time is {datetime.datetime.now().strftime('%H:%M:%S')}."

def check_file_exists(file_path):
    """Checks if a file exists on the system."""
    exists = os.path.exists(file_path)
    return f"File '{file_path}' exists: {exists}."

def list_directory(dir_path="."):
    """Lists files in a directory."""
    try:
        # Resolve to project root if it looks like a relative path from there
        if not os.path.isabs(dir_path):
            dir_path = os.path.join(os.getcwd(), dir_path)
            
        files = os.listdir(dir_path)
        return f"Files in '{dir_path}': {', '.join(files[:10])}" + ("..." if len(files) > 10 else "")
    except Exception as e:
        return f"Error listing directory: {str(e)}"

# Registry of available tools
TOOLS = {
    "get_time": get_time,
    "check_file_exists": check_file_exists,
    "list_directory": list_directory
}

def auto_trigger_tools(text):
    """
    Proactively triggers tools based on intent keywords if no explicit command is found.
    """
    results = []
    text_lower = text.lower()
    
    # 1. Time intent
    if "time" in text_lower:
        res = get_time()
        logger.info(f"✨ Auto-triggered time: {res}")
        results.append(f"[AUTO_TOOL: {res}]")
        
    # 2. File exists intent
    if "check" in text_lower and "file" in text_lower:
        # Try to find a filename
        import re
        file_match = re.search(r"['\"]?(.*?\.[a-z0-9]+)['\"]?", text_lower)
        if file_match:
            path = file_match.group(1).strip()
            res = check_file_exists(path)
            logger.info(f"✨ Auto-triggered file check: {res}")
            results.append(f"[AUTO_TOOL: {res}]")
            
    # 3. List directory intent
    if ("list" in text_lower or "files" in text_lower) and ("directory" in text_lower or "folder" in text_lower or "src" in text_lower):
        # Try to find a dir name
        import re
        dir_match = re.search(r"['\"]?(src|docs|tests|config|data|models|logs)['\"]?", text_lower)
        path = dir_match.group(1) if dir_match else "."
        res = list_directory(path)
        logger.info(f"✨ Auto-triggered ls: {res}")
        results.append(f"[AUTO_TOOL: {res}]")

    return results

def process_tool_calls(text):
    """
    Scans for /time, /exists <path>, /ls <path> commands AND auto-triggers.
    """
    lines = text.split("\n")
    results = []
    
    # Explicit commands
    for line in lines:
        line_clean = line.strip().lower()
        if line_clean.startswith("/time"):
            results.append(f"[TOOL_RESULT: {get_time()}]")
        elif "/exists" in line_clean:
            # Handle cases where it might not be at the start
            parts = line_clean.split("/exists")
            path = parts[1].strip().strip("'").strip('"').split(" ")[0]
            results.append(f"[TOOL_RESULT: {check_file_exists(path)}]")
        elif "/ls" in line_clean:
            parts = line_clean.split("/ls")
            path = parts[1].strip().strip("'").strip('"').split(" ")[0]
            results.append(f"[TOOL_RESULT: {list_directory(path)}]")
            
    # Fallback to auto-trigger if no results yet
    if not results:
        results = auto_trigger_tools(text)
            
    return results
