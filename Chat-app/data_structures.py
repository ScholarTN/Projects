# ════════════════════════════════════════════════════════
#  DATA STRUCTURES
# ════════════════════════════════════════════════════════

# ── 1. Array ─────────────────────────────────────────────
class MessageArray:
    """Dynamic array storing all messages in a room"""
    def __init__(self):
        self._data = []

    def append(self, item):
        self._data.append(item)

    def remove(self, item):
        if item in self._data:
            self._data.remove(item)

    def get_all(self):
        return list(self._data)

    def size(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def clear(self):
        self._data = []


# ── 2. Stack ─────────────────────────────────────────────
class MessageStack:
    """LIFO stack — used to undo/delete last message"""
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        return self._data.pop() if self._data else None

    def peek(self):
        return self._data[-1] if self._data else None

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


# ── 3. Linked List ───────────────────────────────────────
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Singly linked list — maintains ordered message chain"""
    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = node
        self._size += 1

    def remove_last(self):
        if not self.head:
            return None
        if not self.head.next:
            removed = self.head.data
            self.head = None
            self._size -= 1
            return removed
        curr = self.head
        while curr.next and curr.next.next:
            curr = curr.next
        removed = curr.next.data
        curr.next = None
        self._size -= 1
        return removed

    def to_list(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def size(self):
        return self._size

    def is_empty(self):
        return self._size == 0


# ── 4. Hash Map ──────────────────────────────────────────
class HashMap:
    """Hash map — stores username → message count & profile"""
    def __init__(self):
        self._map = {}

    def set(self, key, value):
        self._map[key] = value

    def get(self, key, default=None):
        return self._map.get(key, default)

    def delete(self, key):
        self._map.pop(key, None)

    def keys(self):
        return list(self._map.keys())

    def values(self):
        return list(self._map.values())

    def items(self):
        return list(self._map.items())

    def contains(self, key):
        return key in self._map

    def size(self):
        return len(self._map)


# ── 5. Hash Set ──────────────────────────────────────────
class HashSet:
    """Hash set — tracks unique active users (no duplicates)"""
    def __init__(self):
        self._data = set()

    def add(self, item):
        self._data.add(item)

    def remove(self, item):
        self._data.discard(item)

    def contains(self, item):
        return item in self._data

    def get_all(self):
        return list(self._data)

    def size(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0
