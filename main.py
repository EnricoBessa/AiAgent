from ollama import Ollama
from langchain.schema import HumanMessage
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

def main():
    model = Ollama(model="llama2")

    tools = []
    agent_executor = create_react_agent(model, tools)

    print("Welcome :)")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "quit":
            break

        response = agent_executor.run([HumanMessage(content=user_input)])
        print("\nAssistant:", response)

        for chunk in model.stream_chat([{"role": "user", "content": user_input}]):
            print(chunk, end="")

        # print("\n Assistant: ", end="")

        # for chunk in agent_executor.stream({"messages": [HumanMessage(content = user_input)]}):
        #     if "agent" in chunk and "messages" in chunk["agent"]:
        #         for message in chunk["agent"]["message"]:
        #             print(message.content, end="")

        # print()

if __name__ == "__main__":
    main()