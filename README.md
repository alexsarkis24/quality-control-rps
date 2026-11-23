# Rock Paper Scissors + Stocks Dashboard (CLI and Web App)

![Tests](https://github.com/alexsarkis24/quality-control-rps/actions/workflows/pytest.yml/badge.svg)

A Python app with a command-line game, a stocks dashboard, and a Flask web app, with automated tests and continuous integration (GitHub Actions).

**Live site:** _deployment link added after first deploy_

- `app/rps.py`: rock, paper, scissors game (reusable, tested functions)
- `app/stocks.py`: stocks dashboard using the AlphaVantage API
- `web_app/`: Flask web app (home, RPS and stocks routes, Bootstrap layout, flash messages)
- `test/`: pytest tests that import and invoke the app code
- `.github/workflows/pytest.yml`: CI that runs the tests on every push and pull request

## Setup

Clone the repo and navigate into it:

```sh
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

Create and activate a virtual environment (Python 3.11+):

```sh
# with venv:
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# or with conda:
conda create -n qc-env python=3.11
conda activate qc-env
```

Install packages:

```sh
pip install -r requirements.txt
```

## Configuration (stocks dashboard only)

Get an AlphaVantage API key (from the course page, or <https://www.alphavantage.co/support/#api-key>). Create a local `.env` file (it is git-ignored and must never be committed):

```sh
cp .env.example .env
# then edit .env:
ALPHAVANTAGE_API_KEY="your-key-here"
SECRET_KEY="any-long-random-string"   # used by the web app to sign flash messages
```

## Usage

Play rock, paper, scissors:

```sh
python -m app.rps
```

Run the stocks dashboard (prompts for a symbol, default NFLX, and opens a chart):

```sh
python -m app.stocks
```

### Web App

Run the web app locally, then open <http://localhost:5000/>:

```sh
FLASK_APP=web_app flask run
```

Pages:

- `/`, `/about`, `/hello?name=You`: home routes
- `/rps/form` → `/rps/results`: pick a move from a dropdown and see the result
- `/stocks/form` → `/stocks/dashboard`: enter a symbol to see a price table and chart (also works as `/stocks/dashboard?symbol=MSFT`)

Invalid RPS choices or stock symbols show a flash message and redirect back to the form.

## Testing

```sh
pytest
```

The stocks and web app tests mock the network call, so they run offline and need no API key. That keeps CI secure and deterministic.

## Continuous Integration

GitHub Actions (`.github/workflows/pytest.yml`) installs `requirements.txt` and runs `pytest` on every push to `main` and on every pull request. No secrets are required.

## Deployment (Render)

The app runs in production with gunicorn:

```sh
gunicorn "web_app:create_app()"
```

To deploy on [Render](https://render.com/):

1. New → Web Service → connect this GitHub repository.
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn "web_app:create_app()"`
4. Environment variables: `ALPHAVANTAGE_API_KEY` (your key) and `SECRET_KEY` (a long random string). Set these in Render's dashboard, never in the repo.

## Contributing workflow

Work on a branch, open a pull request into `main`, wait for the CI check to pass, then merge.
