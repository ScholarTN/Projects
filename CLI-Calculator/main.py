import os
from calculator import Calculator

# ── Display helpers ──────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def divider(char="─", width=50):
    print(char * width)

def header():
    clear()
    divider("═")
    print("  🧮  CLI CALCULATOR  |  Stack & Array Edition")
    divider("═")

def print_menu():
    print("""
  OPERATIONS
  ──────────────────────────────────────
  Enter expression:  3 + 5   or   3 + 5 * 2
  Operators:  +  -  *  /  %  ^ (power)

  COMMANDS
  ──────────────────────────────────────
  history  →  View all calculations
  undo     →  Undo last calculation
  clear    →  Clear all history
  help     →  Show this menu
  exit     →  Quit
  ──────────────────────────────────────""")

def show_history(calc):
    divider()
    history = calc.get_history()
    if history:
        print(f"  📚 Calculation History ({len(history)} entries)")
        divider()
        for i, entry in enumerate(history, 1):
            print(f"  {i:>3}. {entry['expression']} = {entry['result']}")
        divider()
        print(f"  Stack depth: {calc.undo_stack.size()} | Array size: {calc.history.size()}")
    else:
        print("  📭 No history yet.")
    divider()

def show_result(expression, result):
    divider()
    print(f"  ✅  {expression} = {result}")
    divider()

def show_error(msg):
    divider()
    print(f"  ❌  Error: {msg}")
    divider()

# ── Main Loop ────────────────────────────────────────────────────

def main():
    calc = Calculator()
    last_result = None

    header()
    print_menu()

    while True:
        try:
            user_input = input("\n  > ").strip()

            if not user_input:
                continue

            # Commands
            if user_input.lower() == "exit":
                print("\n  👋 Goodbye!\n")
                break

            elif user_input.lower() == "help":
                header()
                print_menu()

            elif user_input.lower() == "history":
                show_history(calc)

            elif user_input.lower() == "clear":
                calc.clear_history()
                last_result = None
                print("  🗑️  History cleared.")

            elif user_input.lower() == "undo":
                undone = calc.undo()
                if undone:
                    print(f"  ↩️  Undone: {undone['expression']} = {undone['result']}")
                    print(f"  Stack depth now: {calc.undo_stack.size()}")
                else:
                    print("  ⚠️  Nothing to undo.")

            # Support "ans" keyword for last result
            elif "ans" in user_input.lower():
                if last_result is None:
                    show_error("No previous result (ans) available yet.")
                else:
                    expr = user_input.lower().replace("ans", str(last_result))
                    result = calc.evaluate_expression(expr)
                    last_result = result
                    show_result(user_input + f" (ans={last_result})", result)

            # Simple expression: "3 + 5" or "3 + 5 * 2"
            else:
                parts = user_input.split()

                # Try simple: a op b
                if len(parts) == 3:
                    try:
                        a, op, b = parts
                        result = calc.calculate(a, op, b)
                        last_result = result
                        show_result(f"{a} {op} {b}", result)
                        continue
                    except Exception:
                        pass  # fall through to expression evaluator

                # Multi-term expression: 3 + 5 * 2
                result = calc.evaluate_expression(user_input)
                last_result = result
                show_result(user_input, result)

        except ZeroDivisionError as e:
            show_error(str(e))
        except ValueError as e:
            show_error(str(e))
        except KeyboardInterrupt:
            print("\n\n  👋 Goodbye!\n")
            break


if __name__ == "__main__":
    main()
