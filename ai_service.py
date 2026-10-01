import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

def get_budget_advice(income, expenses, savings_goal):
    if not client:
        return "Gemini API key is not configured. Copy .env.example to .env and add your GEMINI_API_KEY."
    prompt = f"""
You are PocketSmart AI, a friendly budgeting assistant.

User monthly income: ₹{income}
Total expenses: ₹{expenses}
Savings goal: ₹{savings_goal}

Calculate remaining money and provide:
1. Savings feasibility
2. Spending observations
3. Practical budgeting suggestions

Keep it simple. This is general financial education, not professional financial advice.
"""
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    return response.text

def ask_ai(question):
    if not client:
        return "Gemini API key is not configured. Copy .env.example to .env and add your GEMINI_API_KEY."
    prompt = f"""
You are PocketSmart AI, a budgeting assistant.
Answer this question clearly and simply:
{question}
Focus on budgeting, saving, expense tracking and general financial education.
Do not claim to be a professional financial advisor.
"""
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    return response.text
