from langchain.tools import tool

@tool
def git_tools(userid: int, limit: int =10) -> str:
    """Get the lastest commits from github from the userid matching the query
    Args: 
        user: User id of the engineer 
        limit: Maximum number of result to return
    """


    return f"Found {limit} commits for the users {userid}"
