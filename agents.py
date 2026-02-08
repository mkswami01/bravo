from langchain.agents import create_agent
from tools.tickets_tool import search_tickets
from tools.git_tools import git_log
from tools.code_tools import search_code 

SYSTEM_PROMPT = f"""
      You are a helpful agent - Your name is Bravo! Be friendly
      You help engineers find information about tickets, git commits, and code.
      """
agent = create_agent(
    model="gpt-3.5-turbo",
    system_prompt= SYSTEM_PROMPT,
    tools =[git_log,search_code,search_tickets]
)

