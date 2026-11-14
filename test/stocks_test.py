import pandas as pd
import pytest

from app import stocks


def fake_df():
    return pd.DataFrame({"timestamp": ["2025-01-02", "2025-01-03"], "close": [100.0, 105.5]})


def test_format_usd():
    assert stocks.format_usd(1234.5) == "$1,234.50"


def test_get_api_key_missing(monkeypatch):
    monkeypatch.delenv("ALPHAVANTAGE_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        stocks.get_api_key()


def test_build_request_url():
    url = stocks.build_request_url("GOOGL", "abc")
    assert "symbol=GOOGL" in url and "apikey=abc" in url and "datatype=csv" in url


def test_fetch_stocks_csv(monkeypatch):
    """Uses a mocked API so the test is fast, offline, and needs no real key."""
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "fake-key")
    called = {}

    def fake_read_csv(url):
        called["url"] = url
        return fake_df()

    monkeypatch.setattr(stocks, "read_csv", fake_read_csv)
    df = stocks.fetch_stocks_csv("GOOGL")
    assert "symbol=GOOGL" in called["url"]
    assert list(df.columns) == ["timestamp", "close"]


def test_fetch_stocks_csv_bad_response(monkeypatch):
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "fake-key")
    monkeypatch.setattr(stocks, "read_csv", lambda url: pd.DataFrame({"Error Message": ["bad"]}))
    with pytest.raises(ValueError):
        stocks.fetch_stocks_csv("???")


def test_latest_close():
    assert stocks.latest_close(fake_df()) == 105.5
