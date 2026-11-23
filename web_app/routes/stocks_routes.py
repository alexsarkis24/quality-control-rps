from flask import Blueprint, flash, redirect, render_template, request

from app.stocks import DEFAULT_SYMBOL, fetch_stocks_csv, format_usd, latest_close

stocks_routes = Blueprint("stocks_routes", __name__)


@stocks_routes.route("/stocks/form")
def stocks_form():
    return render_template("stocks_form.html", default_symbol=DEFAULT_SYMBOL)


# supports POST from the form and GET like /stocks/dashboard?symbol=MSFT
@stocks_routes.route("/stocks/dashboard", methods=["GET", "POST"])
def stocks_dashboard():
    params = request.form if request.method == "POST" else request.args
    symbol = (params.get("symbol") or DEFAULT_SYMBOL).strip().upper()

    try:
        df = fetch_stocks_csv(symbol).sort_values("timestamp", ascending=False)
    except Exception as err:
        print("STOCKS ERROR:", err)
        flash(f"Couldn't get market data for '{symbol}'. Please check the symbol and try again.", "danger")
        return redirect("/stocks/form")

    flash(f"Fetched market data for {symbol}.", "success")
    records = df.to_dict("records")
    return render_template(
        "stocks_dashboard.html",
        symbol=symbol,
        latest_close_usd=format_usd(latest_close(df)),
        latest_date=records[0]["timestamp"],
        data=records,
    )
