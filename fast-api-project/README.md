# 🎓 Student Record Manager
### FastAPI + Google Sheets + Groq AI

A full-stack student record management system built with **FastAPI**, **Google Sheets** as a live database (via Sheet.best), and **Groq AI** for natural language queries over your data.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 📋 View Students | Live table pulled from Google Sheets |
| ➕ Add Student | Form with full input validation |
| ✏️ Edit Student | Update age or grade inline |
| 🗑️ Delete Student | Remove a record with confirmation |
| 🔍 Search & Filter | Filter by name, grade, and age range |
| ↕️ Sort Columns | Click any column header to sort |
| ⬇️ Export CSV | Download all student data as a CSV file |
| 🤖 Ask Groq AI | Ask natural language questions about your data |

---

## 🛠️ Tech Stack

- **Backend** — [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database** — Google Sheets via [Sheet.best](https://sheet.best) REST API
- **AI** — [Groq](https://console.groq.com) (llama-3.3-70b-versatile)
- **Frontend** — Vanilla HTML/CSS/JS (dark UI, no frameworks)

---

## 📁 Project Structure

```
p1_fastapi_groq_sheets/
├── main.py            # FastAPI app & all API routes
├── sheets.py          # Google Sheets CRUD via Sheet.best
├── groq_ai.py         # Groq AI question answering
├── requirements.txt   # Python dependencies
├── .env               # API keys (not committed to git)
├── .gitignore
└── static/
    └── index.html     # Frontend UI
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/p1-fastapi-groq-sheets.git
cd p1-fastapi-groq-sheets
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up Google Sheets
1. Create a Google Sheet with columns: `Name`, `Age`, `Grade`
2. Make the sheet **public** (Share → Anyone with the link → Viewer)
3. Go to [sheet.best](https://sheet.best) → New Connection → paste your sheet URL
4. Copy the generated API URL

### 5. Get a Groq API Key
1. Sign up free at [console.groq.com](https://console.groq.com)
2. Go to API Keys → Create API Key

### 6. Configure environment variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
SHEETBEST_URL=https://api.sheetbest.com/sheets/your-sheet-id
```

### 7. Run the server
```bash
uvicorn main:app --reload
```

### 8. Open the app
- **UI:** http://127.0.0.1:8000
- **API Docs:** http://127.0.0.1:8000/docs

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/students` | Get all students |
| `POST` | `/students` | Add a new student |
| `PATCH` | `/students/{name}` | Update a student by name |
| `DELETE` | `/students/{name}` | Delete a student by name |
| `POST` | `/ask` | Ask Groq AI about the data |

### Example: Ask AI
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Who has the highest grade?"}'
```

---

## 🔒 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |
| `SHEETBEST_URL` | Your Sheet.best connection URL |

> ⚠️ Never commit your `.env` file to GitHub. It is listed in `.gitignore`.

---

## 📄 License
MIT
