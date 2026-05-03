import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

from crewai import Agent, LLM
from tools import get_stock_data, web_search

# --- Initialize the Native CrewAI LLM ---
# By prefixing with "groq/", CrewAI knows exactly which API key to use
groq_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    temperature=0,
    max_tokens=1024
)

# --- Define the Harvester (Agent 1) ---
data_harvester = Agent(
    role="Senior Market Data Engineer",
    goal="Scrape real-time financial metrics and recent news for a given ticker.",
    backstory=(
        "You are a relentless, unopinionated data gatherer. "
        "You do not analyze; you only fetch accurate, real-time numbers."
    ),
    tools=[get_stock_data, web_search],  # Using our two custom bulletproof tools
    llm=groq_llm,
    allow_delegation=False,
    max_iter=3,
    verbose=True,
)

# --- Define the Analyst (Agent 2) ---
equity_analyst = Agent(
    role="Wall Street Quantitative Analyst",
    goal="Synthesize raw stock data and news into a coherent bullish and bearish narrative for {ticker}.",
    backstory=(
        "You are a ruthless, top-tier Wall Street quantitative analyst. "
        "You despise generic filler words. You focus strictly on numbers, revenue growth, "
        "and concrete market catalysts. If the P/E ratio is above 25, you aggressively question the valuation. "
        "You write in short, punchy, institutional-grade sentences."
    ),
    tools=[], # No tools. It must rely on Agent 1's data.
    llm=groq_llm,
    allow_delegation=False,
    verbose=True,
)

# --- Define the Risk Manager (Agent 3) ---
risk_manager = Agent(
    role="Chief Risk Officer",
    goal="Review the Analyst's draft for {ticker}, identify blind spots, format a final Investment Memo in Markdown, and issue a Buy/Hold/Sell rating.",
    backstory=(
        "You are the Chief Risk Officer for a multi-billion dollar hedge fund. "
        "You have zero tolerance for AI hallucination or fluff. Your job is to ensure every claim "
        "in the final memo is backed by the exact data provided. You strip out emotional language "
        "and format the final output as a sterile, highly professional executive document."
    ),
    tools=[], # No tools.
    llm=groq_llm,
    allow_delegation=False,
    verbose=True,
)