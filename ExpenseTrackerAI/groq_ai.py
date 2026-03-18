import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_groq(question: str, expenses: list, summary: dict) -> str:
    """Send expense data + question to Groq and get a financial insight"""

    if not expenses:
        return "No expense data available yet. Add some expenses first!"

    # Format expenses as readable text
    expense_lines = "\n".join([
        f"- {e.get('Date','?')} | {e.get('Title','?')} | ${e.get('Amount','?')} | {e.get('Category','?')} | {e.get('Notes','')}"
        for e in expenses
    ])

    # Format summary
    summary_lines = "\n".join([
        f"- {cat}: ${amt}" for cat, amt in summary.get("by_category", {}).items()
    ])

    prompt = f"""You are a smart personal finance assistant. Here is the user's expense data:

EXPENSES:
{expense_lines}

SPENDING SUMMARY BY CATEGORY:
{summary_lines}
Total Spent: ${summary.get('total', 0)}

Answer the following question based only on this data. Be concise, helpful, and where relevant give actionable financial advice:
{question}"""

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return response.choices[0].message.content
