from flask import Flask, render_template, request, redirect
from database import (
    init_db, add_expense, get_expenses,
    get_total_expenses, get_category_totals
)
from ai_service import get_budget_advice, ask_ai

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    income = float(request.args.get("income", 0))
    savings_goal = float(request.args.get("savings", 0))
    total_expenses = get_total_expenses()
    remaining = income - total_expenses
    categories = get_category_totals()
    category_data = [{"category": x["category"], "total": x["total"]} for x in categories]
    return render_template(
        "dashboard.html",
        income=income,
        savings_goal=savings_goal,
        total_expenses=total_expenses,
        remaining=remaining,
        category_data=category_data
    )

@app.route("/expenses", methods=["GET", "POST"])
def expenses():
    if request.method == "POST":
        category = request.form["category"]
        description = request.form["description"]
        amount = float(request.form["amount"])
        add_expense(category, description, amount)
        return redirect("/expenses")
    return render_template("expenses.html", expenses=get_expenses())

@app.route("/recommendations")
def recommendations():
    income = float(request.args.get("income", 0))
    savings = float(request.args.get("savings", 0))
    total_expenses = get_total_expenses()

    advice = get_budget_advice(
        income,
        total_expenses,
        savings
    )

    return render_template(
        "recommendations.html",
        advice=advice,
        income=income,
        savings=savings,
        total_expenses=total_expenses
    )

@app.route("/chat", methods=["GET", "POST"])
def chat():
    answer = None
    if request.method == "POST":
        answer = ask_ai(request.form["question"])
    return render_template("chat.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
