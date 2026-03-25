# 💬 CLI Chat Application
### Arrays · Stacks · Linked Lists · Hash Maps · Hash Sets

A command-line chat application that demonstrates all 5 foundational data structures, each serving a specific real-world role.

---

## 🧩 Data Structure Roles

| Data Structure | Role in App |
|---------------|-------------|
| **Array** | Stores all messages in a room |
| **Stack** | Undo last message (LIFO) |
| **Linked List** | Maintains ordered message chain (HEAD → TAIL) |
| **Hash Map** | Stores user profiles and message counts |
| **Hash Set** | Tracks unique active users (no duplicates) |

---

## ✨ Features

- 💬 Send messages in named chat rooms
- 🏠 Join or create rooms dynamically
- ↩️ Undo your last message (Stack pop)
- 👥 View active users (HashSet)
- 📊 View user stats (HashMap)
- 🔗 View linked list chain (HEAD → TAIL)
- 📚 Live data structure state after every message

---

## 📁 Project Structure

```
p6-chat-app/
├── main.py             # CLI interface + main loop
├── chat.py             # ChatRoom + ChatApp logic
├── data_structures.py  # All 5 data structures implemented
└── README.md
```

---

## ⚙️ Run

```bash
# No dependencies needed!
python main.py
```

---

## 🎮 Commands

| Command | Description |
|---------|-------------|
| `<message>` | Send a message |
| `/rooms` | List all rooms |
| `/join <room>` | Join or create a room |
| `/undo` | Undo your last message |
| `/info` | Show all data structure states |
| `/help` | Show commands |
| `/exit` | Quit |

---

## 📄 License
MIT
