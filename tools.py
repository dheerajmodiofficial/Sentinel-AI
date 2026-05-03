from crewai.tools import tool
import yfinance as yf
from duckduckgo_search import DDGS

@tool("Get Stock Data")
def get_stock_data(ticker: str) -> str:
    """
    Fetches live stock data for a given ticker symbol.
    Returns the current price, P/E ratio, and 52-week high/low.
    Use this tool when you need real financial market data for a company.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Extract metrics with a fallback to 'N/A'
        current_price = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
        pe_ratio      = info.get("trailingPE", "N/A")
        week_52_high  = info.get("fiftyTwoWeekHigh", "N/A")
        week_52_low   = info.get("fiftyTwoWeekLow", "N/A")

        return (
            f"Stock Data for {ticker.upper()}:\n"
            f"  Current Price  : ${current_price}\n"
            f"  P/E Ratio      : {pe_ratio}\n"
            f"  52-Week High   : ${week_52_high}\n"
            f"  52-Week Low    : ${week_52_low}\n"
        )

    except Exception as e:
        return f"Error fetching data for ticker '{ticker}': {str(e)}. Please verify the ticker symbol is valid."

@tool("Web Search")
def web_search(query: str) -> str:
    """
    Searches the web for recent news and current events.
    Use this to find breaking news or qualitative data about a company.
    """
    try:
        with DDGS() as ddgs:
            # Fetch the top 3 results to keep the context window light and fast
            results = list(ddgs.text(f"{query} stock earnings OR catalysts OR insider trading news", max_results=3))
            return str(results)
    except Exception as e:
        return f"Search failed for query '{query}': {str(e)}"