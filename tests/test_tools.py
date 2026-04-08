from src.gpt.pipeline import run_pipeline
import os

def test_tool_use():
    print("\n--- Testing Tool: get_time() ---")
    res1 = run_pipeline("Hey Aura, what time is it right now?")
    print(f"Reply: {res1['reply']}")

    print("\n--- Testing Tool: check_file_exists() ---")
    res2 = run_pipeline("Can you check if there is a file named 'README.md' in this folder?")
    print(f"Reply: {res2['reply']}")

    print("\n--- Testing Tool: list_directory() ---")
    res3 = run_pipeline("What files are in the 'src' directory?")
    print(f"Reply: {res3['reply']}")

if __name__ == "__main__":
    test_tool_use()
