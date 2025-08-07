import streamlit as st
import uuid
from graph.core import build_graph

# Build the graph once
graph = build_graph()

# Set Streamlit page info
st.set_page_config(page_title="Crypto Chatbot", page_icon="📊")
st.title("🧠 Crypto Chatbot with LangGraph")

st.markdown("""
Ask about any cryptocurrency using natural language.  
Examples:
- `What is Ethereum and is it a good buy right now?`
- `Give me price and candlestick data of CHR on 1h with 50 samples.`
- `Tell me fundamental and technical analysis of Solana.`
- `What's the latest news about Bitcoin?`
""")

st.markdown("Ask anything in detail will give you better response")
# Set unique thread_id using UUID per session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Message history state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Reset button
if st.button("🔄 Reset Chat"):
    st.session_state.chat_history = []
    st.session_state.thread_id = str(uuid.uuid4())
    st.success("Chat reset!")

# User input
user_input = st.text_input("💬 Ask your question about any crypto:")

if user_input:
    with st.spinner("Analyzing..."):
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        result = graph.invoke({"messages": user_input}, config=config)
        response = result['messages'][-1].content

        # Add as a single Q&A pair
        st.session_state.chat_history.append({
            "user": user_input,
            "bot": response
        })

# Display in reverse order (latest first)
for interaction in reversed(st.session_state.chat_history):
    st.markdown(f"**🧑 You:** {interaction['user']}")
    st.markdown(f"**🤖 Bot:** {interaction['bot']}")
    st.markdown("---")  # separator

# "what is the reason btc has pumped up and dot has pumped itself.  how btc broken all resistance level so easily and gone up. and remember we are talking about currently. in realtime"