from datetime import datetime
from data_structures import MessageArray, MessageStack, LinkedList, HashMap, HashSet


class Message:
    def __init__(self, username, text, room):
        self.username  = username
        self.text      = text
        self.room      = room
        self.timestamp = datetime.now().strftime("%H:%M:%S")
        self.id        = id(self)

    def __str__(self):
        return f"[{self.timestamp}] {self.username}: {self.text}"


class ChatRoom:
    """A single chat room using all 5 data structures"""
    def __init__(self, name):
        self.name         = name
        self.messages     = MessageArray()    # Array: all messages
        self.undo_stack   = MessageStack()    # Stack: undo last message
        self.message_chain = LinkedList()     # Linked List: ordered chain
        self.user_stats   = HashMap()         # Hash Map: user → stats
        self.active_users = HashSet()         # Hash Set: unique users

    def send_message(self, username, text):
        msg = Message(username, text, self.name)

        # Array — store message
        self.messages.append(msg)

        # Stack — push for undo
        self.undo_stack.push(msg)

        # Linked List — append to chain
        self.message_chain.append(msg)

        # Hash Set — track unique user
        self.active_users.add(username)

        # Hash Map — update user stats
        stats = self.user_stats.get(username, {"count": 0, "joined": msg.timestamp})
        stats["count"] += 1
        stats["last_seen"] = msg.timestamp
        self.user_stats.set(username, stats)

        return msg

    def undo_last(self, username):
        """Undo last message — only if it belongs to this user"""
        last = self.undo_stack.peek()
        if not last:
            return None, "No messages to undo."
        if last.username != username:
            return None, f"You can only undo your own messages. Last message is from {last.username}."

        msg = self.undo_stack.pop()
        self.messages.remove(msg)
        self.message_chain.remove_last()

        # Update user stats
        stats = self.user_stats.get(username)
        if stats:
            stats["count"] = max(0, stats["count"] - 1)
            self.user_stats.set(username, stats)

        return msg, "Message undone."

    def get_messages(self):
        return self.messages.get_all()

    def get_user_stats(self):
        return self.user_stats.items()

    def get_active_users(self):
        return self.active_users.get_all()

    def get_chain(self):
        return self.message_chain.to_list()


class ChatApp:
    """Main app managing multiple chat rooms"""
    def __init__(self):
        self.rooms        = HashMap()    # Hash Map: room name → ChatRoom
        self.all_users    = HashSet()    # Hash Set: all users ever seen
        self.current_user = None
        self.current_room = None

        # Create default rooms
        for name in ["general", "random", "tech"]:
            self.rooms.set(name, ChatRoom(name))

    def login(self, username):
        self.current_user = username.strip()
        self.all_users.add(self.current_user)

    def join_room(self, room_name):
        room_name = room_name.lower().strip()
        if not self.rooms.contains(room_name):
            self.rooms.set(room_name, ChatRoom(room_name))
        self.current_room = room_name
        return self.rooms.get(room_name)

    def get_room(self):
        if not self.current_room:
            return None
        return self.rooms.get(self.current_room)

    def list_rooms(self):
        result = []
        for name in self.rooms.keys():
            room = self.rooms.get(name)
            result.append({
                "name": name,
                "messages": room.messages.size(),
                "users": room.active_users.size()
            })
        return result
