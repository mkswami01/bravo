from dotenv import load_dotenv
load_dotenv() 


from agents import agent

def main():

   response = agent.invoke(
    {'messages':[{"role":"user", "content":"Get the last 20 commits from engineer id - 12345?"}]}
   )

   print(response)


if __name__ == "__main__":
    main()
