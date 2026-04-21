import json
import os
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    api_key=os.environ.get("GOOGLE_API_KEY")
)

@tool
def retrieve_autostream_info():
    """Reads the AutoStream knowledge base and returns product details, plans, and policies."""
    with open("knowledge_base.json", "r") as f:
        return json.load(f)

@tool
def mock_lead_capture(name: str, email: str, platform: str):
    """Captures lead information for high-intent users interested in AutoStream.
    Args:
        name: User's full name
        email: User's email address
        platform: The content platform they use (e.g., YouTube, TikTok, Instagram)
    """
    print(f"Lead captured successfully: {name}, {email}, {platform}")
    return "Lead information submitted successfully."

# Define tools
tools = [retrieve_autostream_info, mock_lead_capture]

# System Prompt
system_prompt = (
    "You are a helpful sales assistant for AutoStream. "
    "1. Greet users warmly. "
    "2. Use the retrieve_autostream_info tool to answer questions about pricing, plans, and policies. "
    "3. If a user shows high intent to buy (e.g., asks about subscribing, features, or says they want it), "
    "collect their Name, Email, and Creator Platform. "
    "4. DO NOT call mock_lead_capture until you have collected all 3 pieces of information: Name, Email, and Creator Platform. "
    "Maintain a professional and helpful tone."
)

# Initialize Memory and Agent
memory = MemorySaver()
app = create_react_agent(
    llm, 
    tools, 
    checkpointer=memory,
    prompt=system_prompt
)

def chat_loop():
    config = {"configurable": {"thread_id": "user_1"}}
    print("AutoStream Assistant (Type 'exit' to quit)")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
            
        for chunk in app.stream({"messages": [("user", user_input)]}, config):
            if "agent" in chunk:
                # Output the assistant's response
                msg = chunk["agent"]["messages"][-1]
                print(f"Assistant: {msg.content}")

if __name__ == "__main__":
    chat_loop()
