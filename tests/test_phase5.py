from src.gpt.pipeline import run_pipeline

def test_rag_and_review():
    print("\n--- Testing RAG (Documentation Retrieval) ---")
    # This should hopefully retrieve context about Phase 5 or Architect mode
    res1 = run_pipeline("What is Phase 5 of your evolution plan?")
    print(f"Reply: {res1['reply']}")

    print("\n--- Testing Snippet Indexing ---")
    code = """
```python
def insecure_function(user_input):
    import sqlite3
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # Vulnerable to SQL injection
    cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")
    return cursor.fetchall()
```
"""
    res2 = run_pipeline(f"Hey Aura, can you remember this code? {code}")
    print(f"Reply: {res2['reply']}")

    print("\n--- Testing Code Review Mode ---")
    res3 = run_pipeline("/review How can I improve the security of the function I just showed you?")
    print(f"Reply: {res3['reply']}")

if __name__ == "__main__":
    test_rag_and_review()
