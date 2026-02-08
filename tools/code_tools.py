import subprocess
from langchain.tools import tool

EXCLUDE_DIRS=[".env", ".gitignore", ".python-version", ".venv", "__pycache__", "langgraph.json"]

@tool()
def search_code(query:str) -> str:
    """Search codebase using grep.
    
    Args:
        query: A single short keyword to search for. 
               Examples: 'git', 'auth', 'login', 'config'
               NOT a phrase or sentence. Just one word.
    """

    cmd = ["grep", "-rn", "--include=*.py", query]

    print(f"Query we are calling {query} ")

    for d in EXCLUDE_DIRS:
        cmd.insert(-2, f"--exclude-dir={d}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout or "No matches found"
