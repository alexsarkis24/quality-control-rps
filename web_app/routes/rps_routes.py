from flask import Blueprint, flash, redirect, render_template, request

from app.rps import VALID_OPTIONS, is_valid_choice, play

rps_routes = Blueprint("rps_routes", __name__)


@rps_routes.route("/rps/form")
def rps_form():
    return render_template("rps_form.html", options=VALID_OPTIONS)


@rps_routes.route("/rps/results", methods=["POST"])
def rps_results():
    user_choice = (request.form.get("user_choice") or "").strip().lower()
    if not is_valid_choice(user_choice):
        flash("Invalid choice. Please pick rock, paper, or scissors.", "danger")
        return redirect("/rps/form")

    computer_choice, outcome = play(user_choice)
    return render_template(
        "rps_results.html",
        user_choice=user_choice,
        computer_choice=computer_choice,
        outcome=outcome,
    )
