# 💼 Job Application Tracker
### FastAPI + PostgreSQL (Supabase) + Flask

A full-stack job application tracker with a FastAPI backend, PostgreSQL database on Supabase, and a Flask frontend.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ➕ Add Applications | Company, role, location, status, date, notes |
| 📋 View All Applications | Searchable, filterable table |
| ✏️ Edit inline | Update status, location, notes |
| 🗑️ Delete | Remove an application |
| 📊 Stats Dashboard | Total, Applied, Interview, Offer, Rejected counts |

---

## 🛠️ Architecture

```
Flask (port 5000)  →  FastAPI (port 8000)  →  PostgreSQL (Supabase)
   Frontend              Backend API               Cloud Database
```

---

## 📁 Project Structure

```
p3-job-tracker/
├── fastapi_app/
│   ├── main.py        # FastAPI routes
│   └── database.py    # SQLAlchemy models + DB connection
├── flask_app/
│   ├── app.py         # Flask routes
│   └── templates/
│       └── index.html # Frontend UI
├── requirements.txt
├── .env               # DB credentials (not committed)
├── .env.example
└── .gitignore
```

---

## ⚙️ Setup

```bash
# 1. Clone & install
git clone https://github.com/YOUR_USERNAME/p3-job-tracker.git
cd p3-job-tracker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Create .env
DATABASE_URL=postgresql://postgres:PASSWORD@db.PROJECT.supabase.co:5432/postgres

# 3. Run FastAPI backend (terminal 1)
cd fastapi_app
uvicorn main:app --reload --port 8000

# 4. Run Flask frontend (terminal 2)
cd flask_app
python app.py
```

- **Frontend:** http://127.0.0.1:5000
- **API Docs:** http://127.0.0.1:8000/docs

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/jobs` | Get all jobs + stats |
| POST | `/jobs` | Add new job |
| PATCH | `/jobs/{id}` | Update job |
| DELETE | `/jobs/{id}` | Delete job |

---

## 📄 License
MIT
