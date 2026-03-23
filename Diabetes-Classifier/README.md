# 🩺 Diabetes Risk Predictor
### Decision Tree Classifier · FastAPI + Gradio

A machine learning web app that predicts diabetes risk using a Decision Tree Classifier trained on the Pima Indians Diabetes Dataset.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 ML Model | Decision Tree Classifier (scikit-learn) |
| ⚡ FastAPI | REST API with /predict and /metrics endpoints |
| 🎨 Gradio | Interactive visual interface with sliders |
| 📊 Metrics | Accuracy, confusion matrix, feature importance |
| 🔍 Prediction | Risk level (Low / Medium / High) + confidence % |

---

## 🛠️ Tech Stack
- **ML** — Scikit-learn (DecisionTreeClassifier)
- **Backend** — FastAPI
- **Frontend** — Gradio
- **Dataset** — Pima Indians Diabetes (via OpenML)

---

## 📁 Project Structure

```
p4-diabetes-classifier/
├── main.py          # FastAPI app + /predict /metrics endpoints
├── model.py         # Model training + evaluation
├── gradio_app.py    # Gradio UI (calls FastAPI)
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Setup & Run

```bash
# Install
pip install -r requirements.txt

# Terminal 1 — FastAPI (trains model on first run)
uvicorn main:app --reload --port 8000

# Terminal 2 — Gradio UI
python gradio_app.py
```

- **Gradio UI:** http://127.0.0.1:7860
- **API Docs:** http://127.0.0.1:8000/docs

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict` | Predict diabetes risk |
| GET | `/metrics` | Model accuracy + confusion matrix |
| GET | `/features` | Feature importance scores |

---

## 📄 License
MIT
