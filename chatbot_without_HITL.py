from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
from typing import TypedDict, Annotated
import requests
import os

load_dotenv()

model=ChatOpenAI(model="gpt-4o-mini")

@tool
def get_stock_price(symbol: str)->dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    api_key=os.environ["STOCK_PRICE_API_KEY"]
    url=f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    res=requests.get(url)
    return res.json()

@tool
def dummy_purchase_stock(symbol: str, quantity: str)->dict:
    """
    Simulate purchasing a given quantity of a stock symbol.

    NOTE: This is a mock implementation:
    - No real brokerage API is called.
    - It simply returns a confirmation payload.
    """

    return {
        "status": "success",
        "message": f"Purchase order placed for {quantity} shares of {symbol}.",
        "symbol": symbol,
        "quantity": quantity,
    }

tools=[get_stock_price, dummy_purchase_stock]
model_with_tools=model.bind_tools(tools)

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState)->ChatState:
    """LLM node that may answer or request a tool call."""
    messages=state["messages"]
    res=model_with_tools.invoke(messages)
    return {"messages": [res]}

tool_node=ToolNode(tools)


graph=StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

checkpointer=MemorySaver()

workflow=graph.compile(checkpointer=checkpointer)


if __name__=="__main__":
    print("📈 Stock Bot with Tools (get_stock_price, purchase_stock)")
    print("Type 'exit' to quit.\n")


    thread_id="1234"
    config={
        "configurable": {
            "thread_id": thread_id
        }
    }

    while True:
        user_input=input("You: ")

        if user_input.lower().strip() in ["exit", "quit"]:
            print("Goodbye!")
            break


        state={
            "messages": [HumanMessage(content=user_input)]
        }

        res=workflow.invoke(state, config)

        last_msg=res["messages"][-1].content

        print(f"AI: {last_msg}")


