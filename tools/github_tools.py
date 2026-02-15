
from sqlite3 import Date
from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv
load_dotenv() 

base_url = f"https://api.github.com/"

@tool
def git_commits(author: str = None) -> list:

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

@tool
def git_pull_requests(state: str = "open") -> list:

    """
    Fetch GitHub pull requests for mkswami01/bravo repo.
    
    Args:
        state: Filter by "open", "closed", or "all" (default: "open")
    
    Returns:
        List of PR dicts with title, number, html_url, state, and updated_at.
    """

    headers = {"Authorization":f"token {os.getenv('GITHUB_API_FINE_GRAIN_ACCESS')}"}
    url = base_url+"/repos/mkswami01/bravo/pulls"
    
    params = {
        "state":state,
        "direction":"asc",
        "per_page":100
        }
    
    try:

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status() 
        pr_list = response.json()

        # Return only essential fields for agent consumption
        return [
            {
                "number": pr["number"],
                "title": pr["title"],
                "html_url": pr["html_url"],
                "state": pr["state"],
                "updated_at": pr["updated_at"]
            }
            for pr in pr_list
        ]
    except requests.exceptions.RequestException as e:
        return [{"error": f"Failed to fetch PRs: {str(e)}"}]

#get_pull_requests("all")

#get_commits("dsalian")
