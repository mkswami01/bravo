from dotenv import load_dotenv
from langchain_core.messages import AIMessage, ToolMessage
load_dotenv() 


from agents import agent

def main():

   response = agent.invoke(
    {'messages':[{"role":"user", "content":"What was the last commit by Manoj"}]}
   )

   print(response["messages"][-1].content)


   print(f"Details are here....................")
   for messages in response["messages"]:
      if isinstance(messages,AIMessage):
         print(f"AI messages - AI Message Content {messages.content} \n argument we are searching is {messages.tool_calls} ")
      if isinstance(messages, ToolMessage):
         print(f"AI messages - tool names  {messages.name} \n )")
         print(f"AI messages - tool calls are {messages.name}")

if __name__ == "__main__":
    main()

