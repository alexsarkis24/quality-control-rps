"""Stocks dashboard: fetches daily prices from AlphaVantage and charts them."""

import os

from dotenv import load_dotenv
from pandas import read_csv

load_dotenv()  # reads the local ".env" file (never committed) into environment variables

DEFAULT_SYMBOL = "NFLX"


def get_api_key():
    """Returns the API key from the environment, or raises if it is missing."""
    key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not key:
        raise RuntimeError("Missing ALPHAVANTAGE_API_KEY. Set it in your local .env file.")
    return key


def format_usd(price):
    """Formats a number like 1234.5 as '$1,234.50'."""
    return f"${price:,.2f}"


def build_request_url(symbol, api_key):
    """Builds the AlphaVantage request URL for a symbol."""
    return (
        "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
        f"&symbol={symbol}&apikey={api_key}&datatype=csv&outputsize=full"
    )


def fetch_stocks_csv(symbol=DEFAULT_SYMBOL):
    """Fetches daily stock data as a pandas DataFrame (columns include timestamp, close)."""
    df = read_csv(build_request_url(symbol, get_api_key()))
    if "close" not in df.columns:
        raise ValueError(f"Unexpected API response for symbol {symbol!r}. Check the symbol and API key.")
    return df


def latest_close(df):
    """Returns the most recent closing price from a stocks DataFrame."""
    return float(df.sort_values("timestamp").iloc[-1]["close"])


if __name__ == "__main__":
    import plotly.express as px

    symbol = (input("Please choose a stock symbol: ").strip().upper()) or DEFAULT_SYMBOL
    stocks_df = fetch_stocks_csv(symbol)
    print(stocks_df.head())
    print("LATEST CLOSE:", format_usd(latest_close(stocks_df)))
    px.line(stocks_df, x="timestamp", y="close", title=f"Stock Prices ({symbol})", height=450).show()
