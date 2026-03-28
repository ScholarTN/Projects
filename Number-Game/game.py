import random
from bst import BST


class NumberGame:
    def __init__(self, low=1, high=100):
        self.low         = low
        self.high        = high
        self.secret      = random.randint(low, high)
        self.bst         = BST()
        self.guesses     = 0
        self.max_guesses = self._calc_max()
        self.won         = False
        self.history     = []   # list of (guess, hint)

    def _calc_max(self):
        """Max guesses = log2(range) + 2  — fair for BST strategy"""
        import math
        return math.ceil(math.log2(self.high - self.low + 1)) + 2

    def guess(self, number):
        """
        Process a guess.
        Returns: (hint, nodes_visited, remaining_guesses)
        hint = 'too_low' | 'too_high' | 'correct'
        """
        self.guesses += 1
        _, nodes_visited = self.bst.search(number)

        if number < self.secret:
            hint = "too_low"
        elif number > self.secret:
            hint = "too_high"
        else:
            hint = "correct"
            self.won = True

        self.bst.insert(number, hint)
        self.history.append((number, hint))

        remaining = self.max_guesses - self.guesses
        return hint, nodes_visited, remaining

    def is_over(self):
        return self.won or self.guesses >= self.max_guesses

    def get_smart_hint(self):
        """Give a smart BST-based range hint"""
        guessed = [g for g, _ in self.history]
        too_lows  = [g for g, h in self.history if h == "too_low"]
        too_highs = [g for g, h in self.history if h == "too_high"]

        low  = max(too_lows)  if too_lows  else self.low
        high = min(too_highs) if too_highs else self.high

        mid = (low + high) // 2
        return low, high, mid

    def get_stats(self):
        return {
            "guesses":    self.guesses,
            "max":        self.max_guesses,
            "tree_size":  self.bst.size,
            "tree_height": self.bst.height(),
            "won":        self.won,
            "secret":     self.secret
        }
