import json
import os
from groq import Groq
from dotenv import load_dotenv
from tools import TOOLS, TOOL_SCHEMAS

load_dotenv()

SYSTEM_PROMPT = """You are a helpful AI assistant with access to tools.

You have these tools available:
- get_current_datetime: Get current date and time
- calculate: Evaluate math expressions
- get_weather: Get weather for a city (simulated)
- search_web: Search the web (simulated results)
- save_note: Save a note to a file
- list_notes: List all saved notes

IMPORTANT RULES:
1. For general knowledge questions (history, facts, people, events, news), answer directly from your knowledge. Do NOT call search_web for these.
2. Only call search_web when the user explicitly asks you to search for something.
3. Only call tools when they are clearly needed.
4. For questions about current news or very recent events, let the user know your knowledge has a cutoff and offer to simulate a search.
5. Always be concise, friendly and helpful.
"""


class Agent:
    def __init__(self):
        self.client  = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model   = "llama-3.3-70b-versatile"
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.tool_calls_made = 0

    def _run_tool(self, tool_name: str, tool_args: dict) -> str:
        if tool_name not in TOOLS:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})
        try:
            result = TOOLS[tool_name](**tool_args)
            self.tool_calls_made += 1
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})

    def chat(self, user_message: str) -> tuple:
        self.history.append({"role": "user", "content": user_message})
        tools_used = []
        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
                max_tokens=1024
            )

            msg = response.choices[0].message
            finish_reason = response.choices[0].finish_reason

            # No tool call — plain text response
            if not msg.tool_calls or finish_reason == "stop":
                answer = msg.content or ""
                self.history.append({"role": "assistant", "content": answer})
                return answer, tools_used

            # Handle tool calls
            tool_calls_payload = [
                {
                    "id":       tc.id,
                    "type":     "function",
                    "function": {
                        "name":      tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in msg.tool_calls
            ]

            self.history.append({
                "role":       "assistant",
                "content":    msg.content or "",
                "tool_calls": tool_calls_payload
            })

            # Execute each tool
            for tc in msg.tool_calls:
                tool_name = tc.function.name
                try:
                    tool_args = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    tool_args = {}

                result = self._run_tool(tool_name, tool_args)
                tools_used.append({"tool": tool_name, "args": tool_args})

                self.history.append({
                    "role":         "tool",
                    "tool_call_id": tc.id,
                    "content":      result
                })

        # Fallback if max iterations hit
        fallback = "I had trouble processing that request. Please try again."
        self.history.append({"role": "assistant", "content": fallback})
        return fallback, tools_used

    def reset(self):
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.tool_calls_made = 0
        print("  🔄 Conversation reset.")
