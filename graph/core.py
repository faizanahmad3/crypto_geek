from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from .state import State
from .memory import memory
from .llm import llm_with_tools, tools
from datetime import datetime

def tool_calling_llm(state: State):
    system_prompt = {
        "role": "system",
        "content": (
            f"""You are a professional crypto analysis assistant. 
            You must combine technical analysis, fundamentals, and real-time data. based on this {datetime.now()}
            Always use tools if needed and provide clear answers."""
        )
    }

    # Prepend to the messages
    messages = [system_prompt] + state["messages"]
    return {"messages": [llm_with_tools.invoke(messages)]}

def build_graph():
    builder = StateGraph(State)

    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges("tool_calling_llm", tools_condition)
    builder.add_edge("tools", "tool_calling_llm")

    return builder.compile(checkpointer=memory)
