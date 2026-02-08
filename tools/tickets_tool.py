import json

from langchain.tools import tool 


@tool
def search_tickets(id:str=None, assignee:str=None, status:str=None) -> list:
    """
        Search across for the tickets, identify the correct tickets based on the filters for analysis

        Args:
            id: An identifier for the ticket.
                Example: MK-01, MK-02

            assignee: An assignee id who is responsibile for the ticket
                Exmaple: mill-01-002 , mill-01-009

            status: The status of the ticket, it can be one of the 3
                    To Do, In Progress, Done
    """
    
    tickets = []
    try:
        with open('./data/ticket.json', 'r') as file:
            tickets = json.load(file)["issues"]
    
    except FileNotFoundError:
        print("Error: The tickets mock data is not found")

    try:
        print(f" id is {id }\n assignee is {assignee}\n status is {status}")
        if id:
            tickets = [t for t in tickets if t["id"] == id]
        if assignee:
            tickets = [t for t in tickets if t["fields"]["status"]["assignee"] == assignee]
        if status:
            tickets = [t for t in tickets if t["fields"]["status"]["name"] == status]

        print(f"Tickets are {tickets}")
        
        return tickets
                    
    except KeyError as e:
        print(f"Error: Issue with mock data/api call reading {e}")

    
