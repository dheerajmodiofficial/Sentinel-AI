import streamlit as st
from crewai import Crew, Process
from agents import data_harvester, equity_analyst, risk_manager
from tasks import fetch_data_task, analyze_data_task, risk_review_task
import os

# Page Config
st.set_page_config(page_title="Sentinel AI", page_icon="🛡️", layout="centered")

# --- THE FIX: BYOK (Bring Your Own Key) Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    user_api_key = st.text_input("Enter your Groq API Key:", type="password")
    st.markdown("[Get a free Groq API key here](https://console.groq.com/keys)")
    st.markdown("---")
    st.write("*Note: We do not store your API key. It is used strictly for this session.*")

st.title("🛡️ Sentinel: Autonomous Equity Research")
st.write("Enter a stock ticker to deploy the AI analyst swarm.")

# UI Input
target_stock = st.text_input("Stock Ticker (e.g., AAPL, NVDA, TSLA):").upper()

if st.button("Deploy Sentinel"):
    if not user_api_key:
        st.error("🚨 Please enter your Groq API Key in the sidebar to deploy the agents.")
    elif not target_stock:
        st.error("🚨 Please enter a stock ticker.")
    else:
        # Inject the user's key into the environment so CrewAI/LiteLLM can use it
        os.environ["GROQ_API_KEY"] = user_api_key

        with st.spinner(f"Deploying swarm for {target_stock}. Scraping web and analyzing financials... (~60 seconds)"):
            try:
                # Assemble the Crew
                sentinel_crew = Crew(
                    agents=[data_harvester, equity_analyst, risk_manager],
                    tasks=[fetch_data_task, analyze_data_task, risk_review_task],
                    process=Process.sequential,
                    max_rpm=2, 
                    verbose=False
                )

                # Run the Swarm
                result = sentinel_crew.kickoff(inputs={'ticker': target_stock})

                # Display the Final Report
                st.success("Analysis Complete.")
                st.markdown("---")
                st.markdown(result.raw)

                # --- THE NEW EXPORT FEATURE ---
                st.download_button(
                    label="📥 Download Report (.md)",
                    data=result.raw,
                    file_name=f"{target_stock}_Sentinel_Report.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"System halted. Error: {e}")
                st.warning("Ensure your API key is valid and you haven't hit your rate limits.")