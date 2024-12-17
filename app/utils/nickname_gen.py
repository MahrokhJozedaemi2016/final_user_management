
from builtins import str
import random

def generate_nickname(separator: str = "-") -> str:
    """
    Generate a URL-safe nickname using a mix of adjectives, verbs, nouns, and a 3-digit number.
    Allows choosing a separator (default: hyphen).
    """
    words = ["clever", "jolly", "jumping", "brave", "flying", "gentle", "dancing"]
    nouns = ["panda", "fox", "tiger", "dolphin", "dragon", "lion", "eagle", "whale"]
    number = random.randint(100, 999)  # Ensures 3-digit format for uniqueness
    
    return f"{random.choice(words)}{separator}{random.choice(nouns)}{separator}{number}"
