# 🌳 Dynamic Tree Simulation — Number Game
### Binary Search Tree · Pure Python

A number guessing game that dynamically builds and visualizes a Binary Search Tree with every guess.

---

## 🧩 How BST is Used

Every guess is inserted into the BST:
- Numbers **lower** than current → **LEFT** subtree
- Numbers **higher** than current → **RIGHT** subtree
- The **inorder traversal** always gives guesses in sorted order

```
Example after guesses: 50(↑), 75(↓), 62(↑), 68(✓)

        ┌── 75 ↓
    └── 50 ↑
            ┌── 68 ✓
        └── 62 ↑
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌳 Live BST | Tree updates and displays after every guess |
| 🎮 4 Difficulties | Easy / Medium / Hard / Extreme |
| 💡 Smart Hints | BST-guided midpoint suggestions |
| 📜 History | Inorder traversal shows all guesses sorted |
| 📊 Stats | Efficiency score, tree height, nodes |
| ⭐ Efficiency | Star rating based on guess count |

---

## 📁 Project Structure

```
p9-number-game/
├── main.py    # Game loop + CLI display
├── game.py    # Game logic + hint engine
├── bst.py     # BST implementation + visualizer
└── README.md
```

---

## ⚙️ Run

```bash
# No dependencies needed!
python main.py
```

---

## 🎮 In-game Commands

| Command | Description |
|---------|-------------|
| `<number>` | Make a guess |
| `tree` | Show current BST state |
| `history` | Show all guesses (inorder) |
| `hint` | Get smart BST midpoint hint |
| `quit` | Reveal answer and quit |

---

## 💡 Optimal Strategy
Always guess the **midpoint** of the remaining range — this is exactly what a BST search does! With this strategy you'll always win within the guess limit.

---

## 📄 License
MIT
