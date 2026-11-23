import pandas as pd
import pytest

from web_app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def fake_df():
    return pd.DataFrame({
        "timestamp": ["2025-01-02", "2025-01-03"],
        "open": [99.0, 101.0], "high": [101.0, 106.0], "low": [98.0, 100.0],
        "close": [100.0, 105.5], "volume": [1000, 2000],
    })


@pytest.mark.parametrize("path", ["/", "/home", "/about", "/hello?name=Test", "/rps/form", "/stocks/form"])
def test_pages_load(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert b"QC Web App" in response.data  # shared layout


def test_hello_uses_name(client):
    assert b"Hello, Test!" in client.get("/hello?name=Test").data


def test_rps_form_has_dropdown(client):
    html = client.get("/rps/form").data
    assert b"<select" in html and b'value="rock"' in html


def test_rps_results(client, monkeypatch):
    monkeypatch.setattr("app.rps.generate_random_choice", lambda: "scissors")
    response = client.post("/rps/results", data={"user_choice": "rock"})
    assert response.status_code == 200
    assert b"ROCK" in response.data and b"SCISSORS" in response.data and b"USER WINS" in response.data


def test_rps_invalid_choice_flashes_and_redirects(client):
    response = client.post("/rps/results", data={"user_choice": "lizard"}, follow_redirects=True)
    assert response.request.path == "/rps/form"
    assert b"Invalid choice" in response.data


def test_stocks_dashboard(client, monkeypatch):
    monkeypatch.setattr("web_app.routes.stocks_routes.fetch_stocks_csv", lambda symbol: fake_df())
    response = client.post("/stocks/dashboard", data={"symbol": "msft"})
    assert response.status_code == 200
    assert b"Stocks Dashboard (MSFT)" in response.data
    assert b"$105.50" in response.data  # latest close
    assert b"<table" in response.data and b"Plotly.newPlot" in response.data


def test_stocks_dashboard_get_params(client, monkeypatch):
    monkeypatch.setattr("web_app.routes.stocks_routes.fetch_stocks_csv", lambda symbol: fake_df())
    assert client.get("/stocks/dashboard?symbol=GOOGL").status_code == 200


def test_stocks_invalid_symbol_flashes_and_redirects(client, monkeypatch):
    def boom(symbol):
        raise ValueError("bad symbol")
    monkeypatch.setattr("web_app.routes.stocks_routes.fetch_stocks_csv", boom)
    response = client.post("/stocks/dashboard", data={"symbol": "NOPE"}, follow_redirects=True)
    assert response.request.path == "/stocks/form"
    assert b"Couldn&#39;t get market data" in response.data
