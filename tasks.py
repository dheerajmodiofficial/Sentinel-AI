from crewai import Task
from agents import data_harvester, equity_analyst, risk_manager

# Task 1: The Scrape
fetch_data_task = Task(
    description=(
        "Extract live stock metrics (Price, P/E, 52-week High/Low) and the top 3 "
        "recent news articles for the stock ticker: {ticker}. "
        "Ensure the data is cleanly formatted so the next agent can read it."
    ),
    expected_output="A clean text summary containing the current stock metrics and 3 recent news headlines.",
    agent=data_harvester,
)

# Task 2: The Analysis
analyze_data_task = Task(
    description=(
        "Read the raw data provided by the Data Harvester for {ticker}. "
        "Write a concise analysis of the financial health and market momentum. "
        "CONSTRAINT 1: You MUST explicitly mention the P/E ratio and Current Price. "
        "CONSTRAINT 2: You MUST extract at least one specific catalyst from the news. If no news is relevant, state 'No actionable news catalysts found.' "
        "CONSTRAINT 3: DO NOT attempt to calculate percentages or mathematical variances (e.g., how far the price is from the 52-week high). Only state the exact raw numbers."
    ),
    expected_output="A 3-paragraph analytical draft detailing bullish and bearish signals using strict raw data.",
    agent=equity_analyst,
)

# Task 3: The Final Polish
risk_review_task = Task(
    description=(
        "Review the Equity Analyst's draft for {ticker}. "
        "Format a final Investment Memo in Markdown. "
        "Sections: 1. Executive Summary 2. Bull Case 3. Bear Case / Risks 4. Final Verdict (Buy/Hold/Sell). "
        "CRITICAL INSTRUCTION 1: You must include direct quotes or specific data points from the news in your Bull/Bear cases. "
        "CRITICAL INSTRUCTION 2: Do NOT perform any math or percentage calculations. State raw data only."
    ),
    expected_output="A highly professional, formatted Markdown investment memo.",
    agent=risk_manager,
)