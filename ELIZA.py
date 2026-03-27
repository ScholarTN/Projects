import re
import random

class Eliza:

    def __init__(self):
        self.memory = []

        self.reflections = {
            "am": "are",
            "was": "were",
            "i": "you",
            "i'd": "you would",
            "i've": "you have",
            "i'll": "you will",
            "my": "your",
            "are": "am",
            "you've": "I have",
            "you'll": "I will",
            "your": "my",
            "yours": "mine",
            "you": "me",
            "me": "you"
        }

        # Keyword rules with priority
        self.keywords = {
            "sorry": {
                "rank": 1,
                "responses": [
                    "Please do not apologize.",
                    "Apologies are not necessary.",
                    "What feelings do you have when you apologize?"
                ]
            },
            "i feel": {
                "rank": 5,
                "decomp": r"i feel (.*)",
                "responses": [
                    "Tell me more about feeling {0}.",
                    "Do you often feel {0}?",
                    "When do you usually feel {0}?"
                ]
            },
            "i am": {
                "rank": 4,
                "decomp": r"i am (.*)",
                "responses": [
                    "How long have you been {0}?",
                    "Why do you think you are {0}?",
                    "How does being {0} make you feel?"
                ]
            },
            "mother": {
                "rank": 3,
                "responses": [
                    "Tell me more about your mother.",
                    "What was your relationship with your mother like?"
                ]
            }
        }

        self.fallback = [
            "Please go on.",
            "Can you elaborate?",
            "How does that make you feel?",
            "Why do you say that?"
        ]

    def reflect(self, fragment):
        words = fragment.lower().split()
        return " ".join(self.reflections.get(word, word) for word in words)

    def respond(self, text):
        text = text.lower()

        # sort keywords by priority (highest first)
        sorted_keywords = sorted(
            self.keywords.items(),
            key=lambda x: x[1]["rank"],
            reverse=True
        )

        for keyword, rule in sorted_keywords:
            if keyword in text:
                
                # If decomposition exists
                if "decomp" in rule:
                    match = re.search(rule["decomp"], text)
                    if match:
                        fragment = self.reflect(match.group(1))
                        response = random.choice(rule["responses"])
                        return response.format(fragment)

                # No decomposition (simple keyword)
                return random.choice(rule["responses"])

        # Memory recall (very primitive)
        if self.memory and random.random() < 0.3:
            return self.memory.pop(0)

        # Default fallback
        return random.choice(self.fallback)


# ---- Run ELIZA ----
bot = Eliza()

print("ELIZA: How do you do. Please tell me your problem.")


while True:
    user = input("YOU: ")
    if user.lower() in ["bye", "quit", "exit"]:
        print("ELIZA: Goodbye.")
        break

    response = bot.respond(user)
    print("ELIZA:", response)
    