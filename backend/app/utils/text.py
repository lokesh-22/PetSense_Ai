import math
import re
from collections import Counter
from hashlib import sha256


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9']+")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def term_frequency(text: str) -> Counter:
    return Counter(tokenize(text))


def cosine_similarity(left: Counter, right: Counter) -> float:
    if not left or not right:
        return 0.0
    common = set(left).intersection(right)
    numerator = sum(left[token] * right[token] for token in common)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def embed_vector(text: str, dimensions: int = 32) -> list[float]:
    vector = [0.0] * dimensions
    for token in tokenize(text):
        digest = sha256(token.encode("utf-8")).digest()
        for index in range(dimensions):
            byte = digest[index % len(digest)]
            vector[index] += (byte / 255.0) - 0.5

    magnitude = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [round(value / magnitude, 6) for value in vector]
