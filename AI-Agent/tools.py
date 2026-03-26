# ════════════════════════════════════════════════════════
#  AGENT TOOLS — functions the AI can call
# ════════════════════════════════════════════════════════
import datetime
import math
import json
import os


def get_current_datetime() -> dict:
    """Get the current date and time"""
    now = datetime.datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day":  now.strftime("%A"),
        "timestamp": str(now)
    }


def calculate(expression: str) -> dict:
    """Safely evaluate a math expression"""
    try:
        allowed = set("0123456789+-*/%^.(). eE")
        if not all(c in allowed for c in expression):
            return {"error": "Invalid characters in expression"}
        safe_expr = expression.replace("^", "**")
        result = eval(safe_expr, {"__builtins__": {}, "math": math}, {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "sqrt": math.sqrt, "pi": math.pi, "e": math.e,
            "log": math.log, "abs": abs, "round": round
        })
        return {"expression": expression, "result": round(float(result), 6)}
    except ZeroDivisionError:
        return {"error": "Division by zero"}
    except Exception as e:
        return {"error": f"Could not evaluate: {str(e)}"}


def get_weather(city: str) -> dict:
    """Simulated weather tool (replace with real API for production)"""
    import random
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Windy", "Clear"]
    temp = random.randint(18, 38)
    return {
        "city": city,
        "temperature_c": temp,
        "temperature_f": round(temp * 9/5 + 32, 1),
        "condition": random.choice(conditions),
        "humidity": f"{random.randint(40, 90)}%",
        "note": "Simulated data — connect a real weather API for production"
    }


def search_web(query: str) -> dict:
    """Simulated web search (replace with real search API)"""
    return {
        "query": query,
        "results": [
            {"title": f"Result 1 for '{query}'", "snippet": f"This is a simulated search result about {query}. In production, connect to a real search API like SerpAPI or DuckDuckGo."},
            {"title": f"Result 2 for '{query}'", "snippet": f"Another simulated result for {query}. Replace this with real web search functionality."},
            {"title": f"Result 3 for '{query}'", "snippet": f"More information about {query} would appear here from a real search engine."}
        ],
        "note": "Simulated results — connect SerpAPI or DuckDuckGo API for production"
    }


def save_note(title: str, content: str) -> dict:
    """Save a note to a local file"""
    try:
        os.makedirs("notes", exist_ok=True)
        filename = f"notes/{title.replace(' ', '_').lower()}.txt"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "w") as f:
            f.write(f"Title: {title}\n")
            f.write(f"Saved: {timestamp}\n")
            f.write("-" * 40 + "\n")
            f.write(content)
        return {"message": f"Note saved!", "file": filename, "title": title}
    except Exception as e:
        return {"error": str(e)}


def list_notes() -> dict:
    """List all saved notes"""
    try:
        if not os.path.exists("notes"):
            return {"notes": [], "message": "No notes saved yet."}
        files = [f for f in os.listdir("notes") if f.endswith(".txt")]
        return {"notes": files, "count": len(files)}
    except Exception as e:
        return {"error": str(e)}


# ── Tool registry — maps tool names to functions ─────────
TOOLS = {
    "get_current_datetime": get_current_datetime,
    "calculate":            calculate,
    "get_weather":          get_weather,
    "search_web":           search_web,
    "save_note":            save_note,
    "list_notes":           list_notes,
}

# ── Tool schemas for Groq function calling ────────────────
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date, time and day of the week",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression. Supports +, -, *, /, %, ^, sqrt, sin, cos, pi, e",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "The math expression to evaluate e.g. '2 + 2' or 'sqrt(16)'"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name e.g. 'London' or 'New York'"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information on any topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "Save a note with a title and content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "title":   {"type": "string", "description": "The title of the note"},
                    "content": {"type": "string", "description": "The content of the note"}
                },
                "required": ["title", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "List all saved notes",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]
