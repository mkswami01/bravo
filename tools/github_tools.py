
from sqlite3 import Date
from langchain.tools import tool
import requests
import os

base_url = f"https://api.github.com/"

@tool
def get_commits(author: str = None) -> list:

    """
        Fetch the git commit for repo and author matching query

        Args:
            repo : repository in the github 
            author : Engineer name who is responsible for commit
    """
    headers = {"Authorization":f"token {os.getenv('GITHUB_API_FINE_GRAIN_ACCESS')}"}
    
    url = base_url+"repos/mkswami01/bravo/commits"
    parameter = {}
    if author is None:
        return []

    response = requests.get(url, headers=headers)
    commits = response.json()

    print(f"Commits as json\n{commits}")

    
    if author:
        commits = [c for c in commits if author.lower() in c["commit"]["author"]["name"].lower()] 

    print(f"Commits {commits}")

    return commits

