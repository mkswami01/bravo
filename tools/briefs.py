from tools.github_tools import git_commits, git_pull_requests
from tools.linear_tools import get_issues_update_since
from langchain.tools import tool


@tool
def daily_brief() -> dict:

    """
        Consolidates the commits, pull requests from github and issues from linear
        for daily briefs

        Returns:
            dict of Commits, Pull Requests and Issues .
    """

    try:
        commits = git_commits.func(daily_briefs=True)
        prs = git_pull_requests.func(daily_briefs=True)
        issues = get_issues_update_since.func()

        return {
              "commits": commits,
              "prs": prs,
              "issues": issues
          }

    except Exception as e:
        print(f"Issue with retrieving daily briefs {e}")




