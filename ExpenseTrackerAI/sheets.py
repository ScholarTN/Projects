import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHEETBEST_URL = os.getenv("SHEETBEST_URL")


def get_all_expenses():
    """Read all expenses from Google Sheet"""
    response = requests.get(SHEETBEST_URL)
    if response.status_code == 200:
        data = response.json()
        # Filter out empty rows
        return [r for r in data if r.get("Title") or r.get("Amount")]
    return []


def add_expense(title: str, amount: float, category: str, date: str, notes: str = ""):
    """Add a new expense to Google Sheet"""
    data = {
        "Title": title,
        "Amount": amount,
        "Category": category,
        "Date": date,
        "Notes": notes
    }
    print(f"[DEBUG] Sending: {data}")
    response = requests.post(SHEETBEST_URL, json=data)
    print(f"[DEBUG] Response: {response.status_code} | {response.text}")
    if response.status_code in (200, 201):
        return {"message": f"Expense '{title}' added successfully!"}
    return {"error": f"Sheet.best error ({response.status_code}): {response.text}"}


def delete_expense(title: str):
    """Delete an expense by title"""
    url = f"{SHEETBEST_URL}/Title/{title}"
    response = requests.delete(url)
    if response.status_code in (200, 201):
        return {"message": f"Expense '{title}' deleted successfully!"}
    return {"error": f"Failed to delete '{title}': {response.text}"}


def update_expense(title: str, amount: float = None, category: str = None, notes: str = None):
    """Update an expense by title"""
    url = f"{SHEETBEST_URL}/Title/{title}"
    data = {}
    if amount is not None:
        data["Amount"] = amount
    if category is not None:
        data["Category"] = category
    if notes is not None:
        data["Notes"] = notes
    response = requests.patch(url, json=data)
    if response.status_code in (200, 201):
        return {"message": f"Expense '{title}' updated successfully!"}
    return {"error": f"Failed to update '{title}': {response.text}"}


def get_summary(expenses: list) -> dict:
    """Calculate spending summary by category"""
    summary = {}
    total = 0
    for e in expenses:
        try:
            amount = float(e.get("Amount", 0))
            category = e.get("Category", "Uncategorized")
            summary[category] = round(summary.get(category, 0) + amount, 2)
            total += amount
        except (ValueError, TypeError):
            continue
    return {"by_category": summary, "total": round(total, 2)}
