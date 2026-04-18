import os
import shutil
import datetime
import platform
import re
import json
from pathlib import Path
from src.utils.logger import logger

# Secure workspace directory
WORKSPACE_DIR = Path("aura_workspace")
WORKSPACE_DIR.mkdir(exist_ok=True)

def create_folder(name: str):
    """Creates a new directory in the workspace."""
    try:
        path = WORKSPACE_DIR / name
        path.mkdir(parents=True, exist_ok=True)
        return f"Successfully created folder: {name} in the aura_workspace."
    except Exception as e:
        return f"Error creating folder: {str(e)}"

def list_files(directory: str = "."):
    """Lists files in a specific workspace directory."""
    try:
        target = WORKSPACE_DIR / directory
        files = os.listdir(target)
        return f"Files in {directory}: " + ", ".join(files) if files else "The directory is empty."
    except Exception as e:
        return f"Error listing files: {str(e)}"

def get_system_status():
    """Returns current time and system info."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Current System Time: {now} | OS: {platform.system()} {platform.release()}"

def create_file(name: str, content: str = ""):
    """Creates a file with specific content."""
    try:
        path = WORKSPACE_DIR / name
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully created file '{name}' with {len(content)} bytes."
    except Exception as e:
        return f"Error creating file: {str(e)}"

# Registry of available tools for the LLM to see
AVAILABLE_TOOLS = {
    "create_folder": create_folder,
    "list_files": list_files,
    "get_system_status": get_system_status,
    "create_file": create_file
}

TOOL_DESCRIPTIONS = [
    {
        "name": "create_folder",
        "description": "Create a new directory on the computer. Useful for organizing notes or projects.",
        "parameters": ["name"]
    },
    {
        "name": "list_files",
        "description": "List all files and folders in a directory.",
        "parameters": ["directory"]
    },
    {
        "name": "get_system_status",
        "description": "Get the current date, time, and operating system information.",
        "parameters": []
    },
    {
        "name": "create_file",
        "description": "Create a new text file with specific content.",
        "parameters": ["name", "content"]
    }
]

def execute_tool(tool_name: str, args: dict):
    """Executes a tool from the registry."""
    if tool_name not in AVAILABLE_TOOLS:
        return f"Error: Tool '{tool_name}' not found."
    
    logger.info(f"🔧 Aura executing tool: {tool_name} with args: {args}")
    try:
        # Map args to function parameters
        return AVAILABLE_TOOLS[tool_name](**args)
    except Exception as e:
        return f"Tool execution failed: {str(e)}"

def process_tool_calls(llm_output: str):
    """
    Scans LLM output for <call tool="name"> {json_args} </call> tags.
    Returns a list of results if tools were executed.
    """
    # Pattern to match tool calls like <call tool="create_folder">{"name": "test"}</call>
    pattern = r'<call tool="(.*?)">(.*?)</call>'
    matches = re.findall(pattern, llm_output, re.DOTALL)
    
    if not matches:
        return None
        
    results = []
    for tool_name, args_str in matches:
        try:
            # Clean up JSON string (remove extra whitespace or newlines)
            args_str_clean = args_str.strip()
            args = json.loads(args_str_clean) if args_str_clean else {}
            
            result = execute_tool(tool_name, args)
            results.append(f"Tool '{tool_name}' result: {result}")
        except Exception as e:
            logger.error(f"Tool parsing failed for '{tool_name}': {e}")
            results.append(f"Tool '{tool_name}' failed: {str(e)}")
            
    return results
