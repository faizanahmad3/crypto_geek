# 🧠 Crypto Chatbot with LangGraph & Streamlit

A smart, AI-powered chatbot for crypto traders and enthusiasts — combining real-time market data, technical/fundamental analysis, and up-to-date news using tools like **Binance API**, **CoinGecko**, **Tavily**, and **OpenAI GPT-4o**. Built with LangGraph and Streamlit.

---
## 🚀 Features

- 🔍 Ask real-time questions like:
  - “What is the price of Bitcoin right now?”
  - “Do technical analysis on Ethereum 1d chart.”
  - “Tell me fundamentals of Solana.”
  - “Get latest news about XRP.”

- 📈 Uses live data from:
  - [CoinGecko](https://www.coingecko.com/)
  - [Tavily](https://www.tavily.com/) (for web search)

- 🧠 Powered by:
  - [OpenAI GPT-4o](https://openai.com/gpt-4o)
  - [LangGraph](https://python.langgraph.dev/)
  - [LangChain](https://www.langchain.com/)
  - [Streamlit](https://streamlit.io/)

---

## 🧩 Project Structure

```

project\_root/
├── app.py                  # Streamlit UI app
├── graph/                  # LangGraph logic (graph building, LLM setup, memory)
│   ├── core.py
│   ├── llm.py
│   ├── memory.py
│   └── state.py
├── tools/                 # Tool wrappers
│   ├── binance.py
│   └── coingecko.py
├── utils/
│   └── config.py
├── .env                   # API keys (not committed)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image build
├── docker-compose.yml     # Docker orchestration
└── README.md

````

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/faizanahmad3/crypto_geek.git
cd crypto-geek
````

### 2. Create `.env` File

Create a `.env` file in the root directory with:

```
OPENAI_API_KEY=your-openai-key
TAVILY_API_KEY=your-tavily-key
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Locally

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🐳 Run with Docker

### Build & Start

```bash
docker compose build
docker compose up
```

### Access the App

Visit: [http://localhost:8501](http://localhost:8501)

---

## ✨ Example Queries

Try asking:

* `"Tell me the technical analysis of ETH with a 1d chart."`
* `"Get latest news on Solana and analyze its buying zone."`
* `"What is the current market cap of Dogecoin?"`
* `"Compare the fundamentals of BTC and ETH."`

---

## 🔐 Environment Variables

| Variable         | Description           |
| ---------------- | --------------------- |
| `OPENAI_API_KEY` | OpenAI GPT-4o API key |
| `TAVILY_API_KEY` | Tavily Search API key |

---

## 📦 Requirements

* Python 3.10+
* Docker (optional but recommended)

---

## 📌 Future Improvements

* Add authentication for user sessions
* Store conversation history in a database
* Add voice/chatbot interface
* Price alert notifications

---

## 📝 License

MIT License

---

## 🙋‍♀️ Questions or Feedback?

Open an issue or contact the author via GitHub!

Or Email me at faizanahmad2468@gmail.com
