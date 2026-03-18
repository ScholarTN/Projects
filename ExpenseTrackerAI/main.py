from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, validator
from typing import Optional
from sheets import get_all_expenses, add_expense, delete_expense, update_expense, get_summary
from groq_ai import ask_groq

app = FastAPI(
    title="AI Expense Tracker",
    description="Full Stack Python + Google Sheets + Groq AI",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Pydantic Models ──────────────────────────────────────────────

class Expense(BaseModel):
    title: str
    amount: float
    category: str
    date: str
    notes: Optional[str] = ""

    @validator("title")
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return round(v, 2)

    @validator("category")
    def category_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Category cannot be empty")
        return v.strip()


class UpdateExpense(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    notes: Optional[str] = None


class Question(BaseModel):
    question: str


# ── Routes ───────────────────────────────────────────────────────

@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/expenses")
def read_expenses():
    """Get all expenses"""
    expenses = get_all_expenses()
    summary = get_summary(expenses)
    return {"total": len(expenses), "expenses": expenses, "summary": summary}


@app.post("/expenses")
def create_expense(expense: Expense):
    """Add a new expense"""
    result = add_expense(
        expense.title, expense.amount,
        expense.category, expense.date, expense.notes
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.patch("/expenses/{title}")
def update_expense_record(title: str, update: UpdateExpense):
    """Update an expense by title"""
    result = update_expense(title, update.amount, update.category, update.notes)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.delete("/expenses/{title}")
def remove_expense(title: str):
    """Delete an expense by title"""
    result = delete_expense(title)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/summary")
def spending_summary():
    """Get spending summary by category"""
    expenses = get_all_expenses()
    return get_summary(expenses)


@app.post("/ask")
def ask_question(body: Question):
    """Ask Groq AI about your expenses"""
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    expenses = get_all_expenses()
    summary = get_summary(expenses)
    answer = ask_groq(body.question, expenses, summary)
    return {"question": body.question, "answer": answer}
