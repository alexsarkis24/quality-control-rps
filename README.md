# Quality Control: Rock Paper Scissors + Stocks Dashboard

![Tests](https://github.com/alexsarkis24/quality-control-rps/actions/workflows/pytest.yml/badge.svg)

A small Python app with automated tests and continuous integration (GitHub Actions).

- `app/rps.py`: rock, paper, scissors game (reusable, tested functions)
- `app/stocks.py`: stocks dashboard using the AlphaVantage API
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

## Testing

```sh
pytest
```

The stocks tests mock the network call, so they run offline and need no API key. That keeps CI secure and deterministic.

## Continuous Integration

GitHub Actions (`.github/workflows/pytest.yml`) installs `requirements.txt` and runs `pytest` on every push to `main` and on every pull request. No secrets are required.

## Contributing workflow

Work on a branch, open a pull request into `main`, wait for the CI check to pass, then merge.
