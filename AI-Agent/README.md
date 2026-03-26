# 🤖 AI Agent with LLM and Function Calling
### Groq LLM · Tool Use · Function Calling

A prototype AI agent powered by Groq LLM that autonomously decides which tools to call based on natural language input.

---

## ✨ Features

| Tool | Description |
|------|-------------|
| 🕐 `get_current_datetime` | Get current date, time, day |
| 🧮 `calculate` | Evaluate math expressions |
| 🌤️ `get_weather` | Get weather for any city |
| 🔍 `search_web` | Search the web (simulated) |
| 📝 `save_note` | Save notes to local files |
| 📋 `list_notes` | List all saved notes |

---

## 🛠️ Tech Stack
- **LLM** — Groq (llama-3.3-70b-versatile)
- **Function Calling** — Groq tool_use API
- **Language** — Pure Python

---

## 📁 Project Structure

```
p7-ai-agent/
├── main.py       # CLI interface
├── agent.py      # Agent loop + tool execution
├── tools.py      # Tool functions + schemas
├── requirements.txt
├── .env          # API key (not committed)
└── notes/        # Saved notes (auto-created)
```

---

## ⚙️ Setup & Run

```bash
pip install -r requirements.txt

# Create .env
GROQ_API_KEY=your_key_here

# Run
python main.py
```

---

## 💬 Example Prompts

```
"What time is it?"
"What is sqrt(144) + 25 * 4?"
"What's the weather in Mumbai?"
"Search for FastAPI tutorials"
"Save a note titled 'Todo' with content 'Finish all 16 projects'"
"List my notes"
```

---

## 📄 License
MIT
