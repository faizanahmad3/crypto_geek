from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from tools import fetch_price, fetch_fundamentals, fetch_technical

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Register tools
tools = [fetch_price, fetch_fundamentals, fetch_technical]

# Create ReAct Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # ReAct style
    verbose=True
)

def run_agent(query: str):
    """Run the agent on a user query."""
    return agent.run(query)
