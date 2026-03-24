# 🧮 CLI Calculator with Arrays & Stacks
### Pure Python · Data Structures · No Dependencies

A command-line calculator that demonstrates core data structures — **Arrays** for history storage and **Stacks** for undo functionality.

---

## ✨ Features

| Feature | Data Structure Used |
|---------|-------------------|
| Calculation history | Array (HistoryArray) |
| Undo last calculation | Stack (LIFO) |
| Multi-term expressions | Expression evaluator |
| `ans` keyword | References last result |
| Clear history | Array + Stack reset |

---

## 🛠️ Data Structures

**Stack (LIFO)** — used for undo:
```python
stack.push(item)   # add to top
stack.pop()        # remove from top (undo)
stack.peek()       # view top without removing
```

**HistoryArray** — used for history:
```python
array.append(item)      # add calculation
array.remove_last()     # sync with undo
array.get_all()         # view all history
```

---

## 📁 Project Structure

```
p5-cli-calculator/
├── main.py         # CLI interface + main loop
├── calculator.py   # Stack, HistoryArray, Calculator classes
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
| `3 + 5` | Simple calculation |
| `3 + 5 * 2` | Multi-term expression |
| `ans + 10` | Use last result |
| `history` | View all calculations |
| `undo` | Undo last calculation |
| `clear` | Clear all history |
| `exit` | Quit |

## Supported Operators
`+`  `-`  `*`  `/`  `%`  `^` (power)

---

## 📄 License
MIT
