import subprocess
from sys import stderr
from langchain.tools import tool

@tool
def git_log(author: str=None, num_of_commits: int=10):
    """
        Tool fetches the commit  and can filter by author
        we are only refering to 
        Args:
            author: An authors name for filters
                    Example: 'Manoj', 'dsalian'
            
            num_of_commits: An integer to limit the fetch the commits 
                    Example: 5,10
    """
    try:
        output = subprocess.run(["git", "log", "--oneline", "-n", str(num_of_commits), "--author", author], capture_output=True, text=True)

        if output.stdout:
            return output.stdout
        elif output.stderr:
            raise Exception("Git logging exception")
    except Exception as e:
        print(f"Exception while reading git document {e}")
   