import string
import random


def uuid(length=8, lower=True):
    """sebbe-approved UUID"""
    # risk of collision
    # mixed case: 8 characters -> 1 in 54 trillion
    # lower case: 8 characters -> 1 in 208 billion

    letters = string.ascii_letters
    if lower:
        letters = letters.lower()
    return ''.join(random.choice(letters) for i in range(length))
