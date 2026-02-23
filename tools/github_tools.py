from langchain.tools import tool
import requests
import os
from datetime import datetime, timezone, timedelta

from config.team import resolve_identity

base_url = f"https://api.github.com/"

@tool
def git_commits(author: str = None, daily_briefs: bool = True) -> list:

    """
        Fetch the git commit for repo and author matching query

        Args:
            author : Engineer name who is responsible for commit
            daily_briefs : This is set to True only for getting daily breifs - last day works

        List:
            Return lists of commits baed on the filters
    """
    headers = {"Authorization":f"token {os.getenv('GITHUB_API_FINE_GRAIN_ACCESS')}"}
    
    url = base_url+"repos/mkswami01/bravo/commits"
    params = {}

    if daily_briefs:
        params["since"] = get_date()

    response = requests.get(url, headers=headers, params=params)
    commits = response.json()

    #print(commits)
    
    if author:
        member = resolve_identity(author)
        if member:
            # Check against all known names
            names = [member["name"].lower(), member["github_username"].lower()] + [a.lower() for a in member["aliases"]]
            commits = [c for c in commits if c["commit"]["author"]["name"].lower() in names]
        else:
            commits = [c for c in commits if author.lower() in c["commit"]["author"]["name"].lower()]
        
    # Return only essential fields for agent consumption
    return [
        {
            "author": c["commit"]["author"]["name"],
            "email": c["commit"]["author"]["email"],
            "commit_date": c["commit"]["author"]["date"],
            "commit_message": c["commit"]["message"],
            "url": c["html_url"]
        }
        for c in commits
    ]

@tool
def git_pull_requests(state: str = "open", daily_briefs: bool = True) -> list:

    """
    Fetch GitHub pull requests for mkswami01/bravo repo.
    
    Args:
        state: "open", "closed", or "all" (default: "open"). 
           Use "all" to include merged/closed PRs.
    
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

    if daily_briefs:
        params["since"] = get_date()
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status() 
        pr_list = response.json()

        updates = []
        for pr in pr_list:
            pr_details = get_pr_details(pr["number"])
            code_change = get_code_changes(pr["number"])
            update = {
                "number": pr["number"],
                "title": pr["title"],
                "html_url": pr["html_url"],
                "state": pr["state"],
                "updated_at": pr["updated_at"],
                "branch": pr["head"]["ref"],
                "author": pr["user"]["login"],
                "pr_details": pr_details,
                "code_changes": code_change
            }
            updates.append(update)

        # Return only essential fields for agent consumption
        return updates
    except requests.exceptions.RequestException as e:
        return [{"error": f"Failed to fetch PRs: {str(e)}"}]


def get_pr_details(pull_id : int) -> list:

    headers = {"Authorization":f"token {os.getenv('GITHUB_API_FINE_GRAIN_ACCESS')}"}
    url = base_url+f"/repos/mkswami01/bravo/pulls/{pull_id}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        pr = response.json()

        pr_details = {
            "additions": pr.get("additions", 0),    # new
            "deletions": pr.get("deletions", 0),    # new
            "changed_files": pr.get("changed_files", 0), 
        }

        # Return only essential fields for agent consumption
        return pr_details
    except requests.exceptions.RequestException as e:
        return [{"error": f"Failed to fetch PRs: {str(e)}"}]


def get_code_changes(pull_id : int) -> list:

    headers = {"Authorization":f"token {os.getenv('GITHUB_API_FINE_GRAIN_ACCESS')}"}
    url = base_url+f"/repos/mkswami01/bravo/pulls/{pull_id}/files"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        files = response.json()
        
        changes = []
        
        for file in files:
            change = {
                "filename":file["filename"],
                "status":file["status"],
                "addition":file["additions"],
                "deletion":file["deletions"],
                "changes":file["changes"]
            }
            changes.append(change)

        # Return only essential fields for agent consumption
        return changes
    except requests.exceptions.RequestException as e:
        return [{"error": f"Failed to fetch PRs: {str(e)}"}]


def get_date():
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    return yesterday.strftime("%Y-%m-%dT%H:%M:%SZ")
