import os
from agent import Agent

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def divider(char="─", width=55):
    print(char * width)

def header():
    clear()
    divider("═")
    print("  🤖  AI AGENT  |  Groq LLM + Function Calling")
    divider("═")

def print_menu():
    print("""
  COMMANDS
  ───────────────────────────────────────────────
  Just chat naturally! The agent picks tools auto.

  /reset    →  Start a new conversation
  /history  →  Show conversation length
  /tools    →  List available tools
  /help     →  Show this menu
  /exit     →  Quit
  ───────────────────────────────────────────────

  EXAMPLE PROMPTS
  ───────────────────────────────────────────────
  "What time is it?"
  "What is 25 * 48 + sqrt(144)?"
  "What's the weather in Tokyo?"
  "Search for Python best practices"
  "Save a note titled 'Ideas' with content 'Build more projects'"
  "List my notes"
  ───────────────────────────────────────────────""")

def print_tools():
    divider()
    print("  🛠️  Available Tools")
    divider()
    tools = [
        ("get_current_datetime", "Get current date and time"),
        ("calculate",            "Evaluate math expressions"),
        ("get_weather",          "Get weather for any city"),
        ("search_web",           "Search the web"),
        ("save_note",            "Save a note to file"),
        ("list_notes",           "List all saved notes"),
    ]
    for name, desc in tools:
        print(f"  • {name:<25} {desc}")
    divider()

def main():
    header()
    print_menu()

    agent = Agent()
    print("\n  ✅ Agent ready! Start chatting...\n")

    while True:
        try:
            user_input = input("  You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "/exit":
                print("\n  👋 Goodbye!\n")
                break

            elif user_input.lower() == "/reset":
                agent.reset()
                continue

            elif user_input.lower() == "/history":
                # Exclude system message
                count = len([m for m in agent.history if m["role"] != "system"])
                print(f"  📜 Conversation has {count} message(s). Tool calls made: {agent.tool_calls_made}")
                continue

            elif user_input.lower() == "/tools":
                print_tools()
                continue

            elif user_input.lower() == "/help":
                header()
                print_menu()
                continue

            # Send to agent
            print("  🤖 Thinking", end="", flush=True)
            response, tools_used = agent.chat(user_input)

            # Show which tools were used
            print("\r", end="")
            if tools_used:
                tool_names = ", ".join(t["tool"] for t in tools_used)
                print(f"  [🛠️  Used: {tool_names}]")

            # Print response
            divider()
            print(f"  Agent: {response}")
            divider()

        except KeyboardInterrupt:
            print("\n\n  👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n  ❌ Error: {e}")


if __name__ == "__main__":
    main()
