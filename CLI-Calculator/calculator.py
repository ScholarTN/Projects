# ── Data Structures ──────────────────────────────────────────────

class Stack:
    """Stack implementation using a list (LIFO)"""
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def to_list(self):
        return list(self._data)


class HistoryArray:
    """Dynamic array to store all calculation history"""
    def __init__(self):
        self._data = []

    def append(self, item):
        self._data.append(item)

    def remove_last(self):
        if len(self._data) > 0:
            self._data.pop()

    def get_all(self):
        return list(self._data)

    def clear(self):
        self._data = []

    def size(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0


# ── Calculator Core ──────────────────────────────────────────────

class Calculator:
    def __init__(self):
        self.history    = HistoryArray()
        self.undo_stack = Stack()

    def calculate(self, a, operator, b):
        """Perform a calculation and store in history + stack"""
        a, b = float(a), float(b)

        if operator == "+":
            result = a + b
        elif operator == "-":
            result = a - b
        elif operator in ("*", "x"):
            result = a * b
        elif operator == "/":
            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero!")
            result = a / b
        elif operator == "%":
            if b == 0:
                raise ZeroDivisionError("Cannot modulo by zero!")
            result = a % b
        elif operator in ("**", "^"):
            result = a ** b
        else:
            raise ValueError(f"Unknown operator: '{operator}'")

        result = int(result) if result == int(result) else round(result, 6)
        entry  = {"expression": f"{self._fmt(a)} {operator} {self._fmt(b)}", "result": result}
        self.history.append(entry)
        self.undo_stack.push(entry)
        return result

    def evaluate_expression(self, expr):
        """Evaluate a full expression like 3 + 5 * 2"""
        try:
            allowed = set("0123456789+-*/%^.(). ")
            if not all(c in allowed for c in expr):
                raise ValueError("Invalid characters")
            result = eval(expr.replace("^", "**"), {"__builtins__": {}}, {})
            result = int(result) if result == int(result) else round(float(result), 6)
            entry  = {"expression": expr.strip(), "result": result}
            self.history.append(entry)
            self.undo_stack.push(entry)
            return result
        except ZeroDivisionError:
            raise ZeroDivisionError("Cannot divide by zero!")
        except Exception:
            raise ValueError(f"Invalid expression: '{expr}'")

    def undo(self):
        item = self.undo_stack.pop()
        if item:
            self.history.remove_last()
        return item

    def get_history(self):
        return self.history.get_all()

    def clear_history(self):
        self.history.clear()
        self.undo_stack = Stack()

    def _fmt(self, n):
        return int(n) if n == int(n) else n
