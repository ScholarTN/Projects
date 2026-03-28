import os
from game import NumberGame

# ── Display helpers ──────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def divider(char="─", width=55):
    print(char * width)

def header():
    clear()
    divider("═")
    print("  🌳  BINARY SEARCH TREE  |  Number Game")
    divider("═")

def print_hint(hint, guess, remaining, low, high, mid):
    divider()
    if hint == "too_low":
        print(f"  📈 {guess} is TOO LOW!  →  Go higher")
        print(f"  🎯 Smart range: {low} — {high}  |  Try: {mid}")
    elif hint == "too_high":
        print(f"  📉 {guess} is TOO HIGH! →  Go lower")
        print(f"  🎯 Smart range: {low} — {high}  |  Try: {mid}")
    else:
        print(f"  🎉 {guess} is CORRECT!")
    print(f"  ⏳ Guesses remaining: {remaining}")
    divider()

def print_tree(game):
    print(f"\n  🌳 BST State (size={game.bst.size}, height={game.bst.height()})")
    divider()
    print("  Legend:  ↑ too low   ↓ too high   ✓ correct")
    divider()
    game.bst.visualize()
    divider()

def print_history(game):
    print("\n  📜 Guess History (BST inorder = sorted order)")
    divider()
    inorder = game.bst.inorder()
    for val, hint in inorder:
        symbol = {"too_low": "↑ LOW ", "too_high": "↓ HIGH", "correct": "✓ WIN "}.get(hint, "?")
        bar_len = int((val / game.high) * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        print(f"  [{symbol}]  {val:>4}  |{bar}| {val}/{game.high}")
    divider()

def print_win(game):
    stats = game.get_stats()
    divider("═")
    print(f"  🏆  YOU WIN!  Secret was: {stats['secret']}")
    divider("═")
    print(f"  📊 Final Stats:")
    print(f"     Guesses taken : {stats['guesses']} / {stats['max']}")
    print(f"     BST size      : {stats['tree_size']} nodes")
    print(f"     BST height    : {stats['tree_height']} levels")
    efficiency = round((1 - stats['guesses'] / stats['max']) * 100)
    print(f"     Efficiency    : {efficiency}%  {'⭐⭐⭐' if efficiency > 60 else '⭐⭐' if efficiency > 30 else '⭐'}")
    divider("═")

def print_loss(game):
    stats = game.get_stats()
    divider("═")
    print(f"  💀  GAME OVER!  The number was: {stats['secret']}")
    divider("═")
    print(f"  You used all {stats['max']} guesses.")
    print(f"  Tip: Use BST strategy — always guess the midpoint!")
    divider("═")

def choose_difficulty():
    print("""
  Choose difficulty:
  ─────────────────────────────────────────
  1. Easy    →  1 to 50    (max ~8 guesses)
  2. Medium  →  1 to 100   (max ~9 guesses)
  3. Hard    →  1 to 500   (max ~11 guesses)
  4. Extreme →  1 to 1000  (max ~12 guesses)
  ─────────────────────────────────────────""")

    choice = input("\n  Pick difficulty (1-4): ").strip()
    ranges = {"1": (1, 50), "2": (1, 100), "3": (1, 500), "4": (1, 1000)}
    return ranges.get(choice, (1, 100))


# ── Main Game Loop ───────────────────────────────────────────────

def play_game(low, high):
    game = NumberGame(low, high)
    header()
    print(f"\n  🎮 Guess a number between {low} and {high}")
    print(f"  ⏳ You have {game.max_guesses} guesses")
    print(f"  💡 Tip: Use BST strategy — guess the midpoint each time!\n")
    print(f"  Commands: 'tree' → show BST | 'history' → show all guesses | 'hint' → get smart hint\n")

    while not game.is_over():
        try:
            raw = input(f"  [{game.guesses+1}/{game.max_guesses}] Your guess: ").strip().lower()

            if raw == "tree":
                print_tree(game)
                continue
            elif raw == "history":
                if game.bst.size > 0:
                    print_history(game)
                else:
                    print("  No guesses yet!")
                continue
            elif raw == "hint":
                if game.bst.size > 0:
                    l, h, mid = game.get_smart_hint()
                    print(f"  💡 Smart hint: try between {l} and {h}  →  midpoint = {mid}")
                else:
                    print(f"  💡 Start with the midpoint: {(low + high) // 2}")
                continue
            elif raw == "quit":
                print(f"\n  The number was: {game.secret}")
                break

            number = int(raw)
            if number < low or number > high:
                print(f"  ⚠️  Please enter a number between {low} and {high}")
                continue

            hint, nodes_visited, remaining = game.guess(number)
            l, h, mid = game.get_smart_hint()
            print_hint(hint, number, remaining, l, h, mid)

            # Always show tree after each guess
            print_tree(game)

        except ValueError:
            print("  ⚠️  Please enter a valid number (or 'tree', 'history', 'hint')")
        except KeyboardInterrupt:
            print(f"\n\n  The number was: {game.secret}\n")
            return False

    # End of game
    if game.won:
        print_win(game)
        print_history(game)
    else:
        print_loss(game)
        print(f"\n  🌳 Final BST:")
        print_tree(game)

    return True


def main():
    while True:
        header()
        print("""
  🌳 HOW IT WORKS:
  ─────────────────────────────────────────
  Every guess you make is inserted into a
  Binary Search Tree (BST):
  • Lower guesses  →  LEFT  subtree
  • Higher guesses →  RIGHT subtree
  • Correct guess  →  ROOT  (marked ✓)

  Use BST strategy: always guess the
  midpoint of the remaining range!
  ─────────────────────────────────────────""")

        low, high = choose_difficulty()
        play_game(low, high)

        again = input("\n  Play again? (y/n): ").strip().lower()
        if again != "y":
            print("\n  👋 Thanks for playing!\n")
            break


if __name__ == "__main__":
    main()
