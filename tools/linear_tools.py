from datetime import datetime, timedelta, timezone
from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
load_dotenv()

linear_graphql_url="https://api.linear.app/graphql"

@tool
def get_issues_by_assignee(assignee:str=None) -> list:

    """

        List the issues assiged to the assign 

        Args:
            assignee: Filter by the name of engineer 

        Return:
            List the issue with the id, identifier , title , state and assignee

    
    """
    query = f"""                                                                                                                                                                                                    
    {{                                                                                                                                                                                                              
        issues(filter: {{ assignee: {{ name: {{ eq: "{assignee}" }} }} }}) {{
            nodes {{
                id
                identifier
                title
                state {{ name }}
                assignee {{ name }}
            }}
        }}
    }}"""
        
    try:
        response = requests.post(
            url=linear_graphql_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": os.getenv("LINEAR_API_KEY")
            },
            json={"query": query}  
        )
        
        # Check for HTTP errors
        response.raise_for_status()

        data = response.json()
        return data["data"]["issues"]["nodes"]
    except Exception as e:
        print(f"Issue fetching linear apis requests {e}")



@tool
def get_issue_by_state(state:str= "In Progress") -> list:
    """
         List the issues by filtering the state  

        Args:
            state: The issue can be in backlogs, Todo, In Progress, Done

        Return:
            List the issue with the id, identifier, title , state and assignee

    """

    query = f"""
    {{
        issues (filter: {{state: {{name: {{eq: "{state}" }} }} }}) {{
            nodes {{
                id
                identifier
                title
                state {{ name }}
                assignee {{ name }}
            }}
        }}
    }}"""

    try:
        response = requests.post(
            url=linear_graphql_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": os.getenv("LINEAR_API_KEY")
            },
            json={"query": query}  
        )

        # Check for HTTP errors
        response.raise_for_status()

        data = response.json()

        
        return data["data"]["issues"]["nodes"]


    except Exception as e:
        print("Issue with the issues filtering by state")

@tool
def get_issues_update_since()-> list:
    
    """
         List the issues from last day and get all the changes

        Return:
            List the issue with the id, identifier, title , state and assignee

    """
    date = get_date()
    print(date)
    query = f"""                                                                                                                                                                                                    
    {{                                                                                                                                                                                                              
        issues(filter: {{ assignee: {{ updatedAt: {{ gte: "{date}" }} }} }}) {{
            nodes {{
                id
                identifier
                title
                state {{ name }}
                assignee {{ name }}
                updatedAt
            }}
        }}
    }}"""
        

    try:
        response = requests.post(
            url=linear_graphql_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": os.getenv("LINEAR_API_KEY")
            },
            json={"query": query}  
        )

        # Check for HTTP errors
        response.raise_for_status()

        data = response.json()
        print(response.status_code)

        
        return data["data"]["issues"]["nodes"]


    except Exception as e:
        print(f"Issue with the issues filtering by state {e}")

def get_date():
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    return yesterday.strftime("%Y-%m-%dT%H:%M:%SZ")
