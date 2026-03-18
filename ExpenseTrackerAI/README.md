# 💸 AI Expense Tracker
### Full Stack Python + Google Sheets + Groq AI

A full-stack personal expense tracking app built with **FastAPI**, **Google Sheets** as a live database, and **Groq AI** for natural language financial insights.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| ➕ Add Expenses | Log title, amount, category, date, notes |
| 📋 View All Expenses | Live table with sorting and filtering |
| ✏️ Edit / 🗑️ Delete | Update or remove any expense |
| 🔍 Search & Filter | Filter by name or category, sort by date/amount |
| 📊 Spending Summary | Live category breakdown cards with percentages |
| ⬇️ Export CSV | Download all expenses as a CSV file |
| 🤖 Ask Groq AI | Get financial insights & budgeting advice |

---

## 🛠️ Tech Stack

- **Backend** — FastAPI (Python)
- **Database** — Google Sheets via Sheet.best REST API
- **AI** — Groq (llama-3.3-70b-versatile) — open source LLM
- **Frontend** — Vanilla HTML/CSS/JS

---

## 📁 Project Structure

```
p2-expense-tracker/
├── main.py          # FastAPI routes + validation
├── sheets.py        # Google Sheets CRUD + summary
├── groq_ai.py       # Groq AI financial assistant
├── requirements.txt
├── .env             # API keys (not committed)
├── .gitignore
└── static/
    └── index.html   # Frontend UI
```

---

## ⚙️ Setup

```bash
# 1. Clone & enter project
git clone https://github.com/YOUR_USERNAME/p2-expense-tracker.git
cd p2-expense-tracker

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
GROQ_API_KEY=your_groq_api_key
SHEETBEST_URL=your_sheetbest_url

# 5. Run
uvicorn main:app --reload
```

Open: http://127.0.0.1:8000

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/expenses` | Get all expenses + summary |
| POST | `/expenses` | Add new expense |
| PATCH | `/expenses/{title}` | Update expense |
| DELETE | `/expenses/{title}` | Delete expense |
| GET | `/summary` | Category spending summary |
| POST | `/ask` | Ask Groq AI |

---

## 🔒 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | From console.groq.com (free) |
| `SHEETBEST_URL` | From sheet.best connection |

> ⚠️ Never commit `.env` to GitHub.

---

## 📄 License
MIT
