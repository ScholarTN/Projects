# ════════════════════════════════════════════════════════
#  BINARY SEARCH TREE
# ════════════════════════════════════════════════════════

class BSTNode:
    def __init__(self, value, hint=None):
        self.value = value
        self.hint  = hint   # "too_low", "too_high", "correct"
        self.left  = None   # smaller values
        self.right = None   # larger values


class BST:
    def __init__(self):
        self.root     = None
        self.size     = 0

    def insert(self, value, hint=None):
        """Insert a guessed number into the BST"""
        node = BSTNode(value, hint)
        if not self.root:
            self.root = node
        else:
            self._insert(self.root, node)
        self.size += 1

    def _insert(self, current, node):
        if node.value < current.value:
            if current.left is None:
                current.left = node
            else:
                self._insert(current.left, node)
        elif node.value > current.value:
            if current.right is None:
                current.right = node
            else:
                self._insert(current.right, node)

    def search(self, value):
        """Search for a value, return (found, nodes_visited)"""
        return self._search(self.root, value, 0)

    def _search(self, node, value, count):
        if node is None:
            return False, count
        count += 1
        if value == node.value:
            return True, count
        elif value < node.value:
            return self._search(node.left, value, count)
        else:
            return self._search(node.right, value, count)

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def inorder(self):
        """Return all values in sorted order"""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.value, node.hint))
            self._inorder(node.right, result)

    def get_path_to(self, value):
        """Get the path taken to find a value"""
        path = []
        self._get_path(self.root, value, path)
        return path

    def _get_path(self, node, value, path):
        if node is None:
            return False
        path.append(node.value)
        if value == node.value:
            return True
        elif value < node.value:
            return self._get_path(node.left, value, path)
        else:
            return self._get_path(node.right, value, path)

    def visualize(self):
        """Print a visual representation of the BST"""
        if not self.root:
            print("  (empty tree)")
            return
        lines = []
        self._build_visual(self.root, "", True, lines)
        for line in lines:
            print(line)

    def _build_visual(self, node, prefix, is_left, lines):
        if node is None:
            return

        # Right subtree first (top of display)
        if node.right:
            new_prefix = prefix + ("│   " if is_left else "    ")
            self._build_visual(node.right, new_prefix, False, lines)

        # Current node with hint indicator
        connector = "└── " if is_left else "┌── "
        hint_symbol = {
            "too_low":  " ↑",
            "too_high": " ↓",
            "correct":  " ✓",
            None: ""
        }.get(node.hint, "")

        lines.append(f"  {prefix}{connector}{node.value}{hint_symbol}")

        # Left subtree (bottom of display)
        if node.left:
            new_prefix = prefix + ("    " if is_left else "│   ")
            self._build_visual(node.left, new_prefix, True, lines)
