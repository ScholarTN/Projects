import os
from chat import ChatApp

# ── Display Helpers ──────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def divider(char="─", width=55):
    print(char * width)

def header(app):
    clear()
    divider("═")
    user = app.current_user or "Not logged in"
    room = f"#{app.current_room}" if app.current_room else "No room"
    print(f"  💬  CHAT APP  |  {user}  |  {room}")
    divider("═")

def print_messages(room):
    msgs = room.get_messages()
    divider()
    if msgs:
        print(f"  📨 Messages in #{room.name} ({len(msgs)} total)")
        divider()
        for msg in msgs:
            print(f"  {msg}")
    else:
        print(f"  📭 No messages in #{room.name} yet.")
    divider()

def print_room_info(room):
    divider()
    print(f"  📊 Room Info: #{room.name}")
    divider()

    # Active users from Hash Set
    users = room.get_active_users()
    print(f"  👥 Active Users (HashSet): {', '.join(users) if users else 'none'}")

    # User stats from Hash Map
    print(f"\n  📈 User Stats (HashMap):")
    for user, stats in room.get_user_stats():
        print(f"     {user:<15} {stats['count']} msg(s)  |  joined: {stats['joined']}")

    # Linked list chain
    chain = room.get_chain()
    print(f"\n  🔗 Message Chain (LinkedList): {room.message_chain.size()} nodes")
    if chain:
        print(f"     HEAD → {chain[0].username}: '{chain[0].text[:30]}'")
        print(f"     TAIL → {chain[-1].username}: '{chain[-1].text[:30]}'")

    # Stack info
    top = room.undo_stack.peek()
    print(f"\n  🥞 Undo Stack (Stack): {room.undo_stack.size()} item(s)")
    if top:
        print(f"     TOP  → {top.username}: '{top.text[:30]}'")

    # Array info
    print(f"\n  📚 Message Array (Array): {room.messages.size()} item(s)")
    divider()

def print_menu():
    print("""
  COMMANDS
  ───────────────────────────────────────────────
  <message>        Send a message
  /rooms           List all rooms
  /join <room>     Join or create a room
  /undo            Undo your last message
  /users           Show users & stats
  /info            Show data structure states
  /clear           Clear screen
  /help            Show this menu
  /exit            Quit
  ───────────────────────────────────────────────""")

def list_rooms(app):
    divider()
    print("  🏠 Available Rooms")
    divider()
    for r in app.list_rooms():
        print(f"  #{r['name']:<15} {r['messages']} msg(s)  |  {r['users']} user(s)")
    divider()

# ── Main Loop ────────────────────────────────────────────────────

def main():
    app = ChatApp()

    clear()
    divider("═")
    print("  💬  WELCOME TO CHAT APP")
    print("  Data Structures: Array · Stack · LinkedList · HashMap · HashSet")
    divider("═")

    # Login
    while not app.current_user:
        username = input("\n  Enter your username: ").strip()
        if len(username) < 2:
            print("  ⚠️  Username must be at least 2 characters.")
            continue
        if " " in username:
            print("  ⚠️  No spaces in username.")
            continue
        app.login(username)

    # Join default room
    app.join_room("general")
    room = app.get_room()

    header(app)
    print_menu()
    print_messages(room)

    while True:
        try:
            user_input = input(f"\n  [{app.current_user}@#{app.current_room}] > ").strip()

            if not user_input:
                continue

            room = app.get_room()

            # ── Commands ──
            if user_input.lower() == "/exit":
                print("\n  👋 Goodbye!\n")
                break

            elif user_input.lower() == "/help":
                header(app)
                print_menu()

            elif user_input.lower() == "/clear":
                header(app)
                print_messages(room)

            elif user_input.lower() == "/rooms":
                list_rooms(app)

            elif user_input.lower().startswith("/join "):
                room_name = user_input[6:].strip()
                if not room_name:
                    print("  ⚠️  Usage: /join <roomname>")
                else:
                    app.join_room(room_name)
                    room = app.get_room()
                    header(app)
                    print(f"  ✅ Joined #{room_name}")
                    print_messages(room)

            elif user_input.lower() == "/undo":
                msg, status = room.undo_last(app.current_user)
                if msg:
                    print(f"  ↩️  Undone: '{msg.text}'")
                    print(f"  Stack depth now: {room.undo_stack.size()}")
                else:
                    print(f"  ⚠️  {status}")

            elif user_input.lower() in ("/users", "/info"):
                print_room_info(room)

            # ── Send message ──
            else:
                if user_input.startswith("/"):
                    print(f"  ⚠️  Unknown command. Type /help for commands.")
                    continue
                msg = room.send_message(app.current_user, user_input)
                print(f"  ✅ {msg}")
                print(f"     [Array: {room.messages.size()} | Stack: {room.undo_stack.size()} | LinkedList: {room.message_chain.size()} | HashSet: {room.active_users.size()} users]")

        except KeyboardInterrupt:
            print("\n\n  👋 Goodbye!\n")
            break


if __name__ == "__main__":
    main()
