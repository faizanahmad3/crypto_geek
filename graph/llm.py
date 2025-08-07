from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
# from tools.binance_api import get_price, get_candlestick_data
from tools.coingecko_api import get_price, get_candlestick_data, get_fundamentals
from utils.config import OPENAI_API_KEY, TAVILY_API_KEY

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Tools
tavily_tool = TavilySearch()
tools = [get_price, get_candlestick_data, get_fundamentals, tavily_tool]

# Bind tools
llm_with_tools = llm.bind_tools(tools)
