import streamlit as st
from crewai import Crew, Process
from agents import data_harvester, equity_analyst, risk_manager
from tasks import fetch_data_task, analyze_data_task, risk_review_task
import os

# Page Config
st.set_page_config(page_title="Sentinel AI", page_icon="🛡️", layout="centered")

st.title("🛡️ Sentinel: Autonomous Equity Research")
st.write("Deploy an AI analyst swarm to generate an institutional-grade investment memo.")
st.markdown("---")

# --- STEP 1: BYOK Configuration ---
st.markdown("### ⚙️ Step 1: Engine Configuration")
user_api_key = st.text_input("Enter your free Groq API Key:", type="password")
st.markdown("*Don't have one? [Get a free key here in 10 seconds](https://console.groq.com/keys). We do not store your key.*")

st.text("") # Blank space for clean UI

# --- STEP 2: The Target ---
st.markdown("### 📊 Step 2: Target Asset")
target_stock = st.text_input("Stock Ticker (e.g., AAPL, NVDA, RELIANCE.NS):").upper()

st.text("") # Blank space for clean UI

# --- STEP 3: Ignition ---
if st.button("Deploy Sentinel", use_container_width=True):
    if not user_api_key:
        st.error("🚨 Please enter your Groq API Key in Step 1 to deploy the agents.")
    elif not target_stock:
        st.error("🚨 Please enter a stock ticker in Step 2.")
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

                # The Export Feature
                st.download_button(
                    label="📥 Download Report (.md)",
                    data=result.raw,
                    file_name=f"{target_stock}_Sentinel_Report.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"System halted. Error: {e}")
                st.warning("Ensure your API key is valid and you haven't hit your rate limits.")