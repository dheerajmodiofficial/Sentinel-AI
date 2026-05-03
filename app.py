import streamlit as st
from crewai import Crew, Process
from agents import data_harvester, equity_analyst, risk_manager
from tasks import fetch_data_task, analyze_data_task, risk_review_task
import os

# Page Config
st.set_page_config(page_title="Sentinel AI", page_icon="🛡️", layout="centered")
st.title("🛡️ Sentinel: Autonomous Equity Research")
st.write("Enter a stock ticker to deploy the AI analyst swarm.")

# UI Input
target_stock = st.text_input("Stock Ticker (e.g., AAPL, NVDA, TSLA):").upper()

if st.button("Deploy Sentinel") and target_stock:
    with st.spinner(f"Deploying swarm for {target_stock}. Scraping web and analyzing financials... (~60 seconds)"):
        try:
            # Assemble the Crew
            sentinel_crew = Crew(
                agents=[data_harvester, equity_analyst, risk_manager],
                tasks=[fetch_data_task, analyze_data_task, risk_review_task],
                process=Process.sequential,
                max_rpm=2, 
                verbose=False # Turn off terminal logging for the UI
            )

            # Run the Swarm
            result = sentinel_crew.kickoff(inputs={'ticker': target_stock})

            # Display the Final Report
            st.success("Analysis Complete.")
            st.markdown("---")
            st.markdown(result.raw) # Render the markdown

        except Exception as e:
            st.error(f"System halted. Error: {e}")
            st.warning("Rate limit hit or connection failed. Please wait 60 seconds and try again.")