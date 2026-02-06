from langchain.agents import create_agent
from tools import git_tools as git_tool

agent = create_agent(
    model="gpt-3.5-turbo",
    system_prompt= "You are a helpful agent - Your name is Bravo! Be friendly",
    tools =[git_tool]
)
