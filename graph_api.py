import os
from dotenv import load_dotenv
from typing import Annotated
from binance_api import get_price, get_candlestick_data
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()
class State(TypedDict):
    messages:Annotated[list, add_messages]

graph_builder = StateGraph(State)

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("llmchatbot", chatbot)
graph_builder.add_edge(START, "llmchatbot")
graph_builder.add_edge("llmchatbot", END)

# graph = graph_builder.compile()
# response = graph.invoke({"messages": "do you know me"})
# print(response)

tools = [get_price, get_candlestick_data]

llm_with_tools = llm.bind_tools(tools)

def tool_calling_llm(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder = StateGraph(State)

graph_builder.add_node("tool_calling_llm", tool_calling_llm)
graph_builder.add_node("tools", ToolNode(tools))

graph_builder.add_edge(START, "tool_calling_llm")
graph_builder.add_conditional_edges("tool_calling_llm", tools_condition)
graph_builder.add_edge("tools", "tool_calling_llm")

graph = graph_builder.compile()
response = graph.invoke({"messages": "give price and candlestick data of DOT of 1h and only 50 samples, and tell me about what is best buying zone and selling zone also give me little information about the resistance."})
print(response)
for m in response['messages']:
    m.pretty_print()
