# # Placeholder (full code in canvas)# tools/utils.py
# from __future__ import annotations
# import re
# from typing import List

# HASHTAG_STOPWORDS = {
# "the","and","a","an","of","in","to","for","with","on","is","are","be","or","by","your","you"
# }

# PLATFORM_LIMITS = {
# "instagram": 2200,
# "twitter": 280, # X
# "linkedin": 3000,
# }

# def extract_keywords(text: str, max_k: int = 6) -> List[str]:
# words = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", text.lower())
# freq = {}
# for w in words:
# if w in HASHTAG_STOPWORDS:
# continue
# freq[w] = freq.get(w, 0) + 1
# ranked = sorted(freq, key=freq.get, reverse=True)
# return [w for w in ranked[:max_k]]


# def make_hashtags(keywords: List[str], limit: int = 8) -> List[str]:
# tags = []
# for k in keywords:
# k_clean = re.sub(r"[^a-z0-9]+", "", k.lower())
# if k_clean and k_clean not in HASHTAG_STOPWORDS:
# tags.append(f"#{k_clean}")
# if len(tags) >= limit:
# break
# return tags


# def enforce_platform_limit(text: str, platform: str) -> str:
# limit = PLATFORM_LIMITS.get(platform, 2200)
# if len(text) <= limit:
# return text
# # try trimming smartly at sentence boundary
# trimmed = text[:limit]
# last_dot = trimmed.rfind(".")
# return (trimmed[: last_dot + 1].strip() if last_dot != -1 else trimmed.strip())

#*******************************************************************************************************


from __future__ import annotations
import re
from typing import List
from collections import Counter

# Using a set is more efficient for "in" checks
HASHTAG_STOPWORDS = {
    "the", "and", "a", "an", "of", "in", "to", "for", "with", 
    "on", "is", "are", "be", "or", "by", "your", "you", "it", "at"
}

PLATFORM_LIMITS = {
    "instagram": 2200,
    "twitter": 280,  # For X
    "linkedin": 3000,
}

def extract_keywords(text: str, max_k: int = 6) -> List[str]:
    """Extracts the most frequent keywords from text, ignoring stopwords."""
    # Use collections.Counter for a more efficient and Pythonic frequency count
    words = re.findall(r"\b[a-zA-Z-]{3,}\b", text.lower())
    words = [word for word in words if word not in HASHTAG_STOPWORDS]
    most_common_words = [word for word, freq in Counter(words).most_common(max_k)]
    return most_common_words

def make_hashtags(keywords: List[str], limit: int = 8) -> List[str]:
    """Creates a list of hashtags from keywords."""
    tags = []
    for k in keywords:
        # Cleaning logic is good, no changes needed here.
        k_clean = re.sub(r"[^a-z0-9]+", "", k.lower())
        if k_clean and k_clean not in HASHTAG_STOPWORDS:
            tags.append(f"#{k_clean}")
        if len(tags) >= limit:
            break
    return tags

def enforce_platform_limit(text: str, platform: str) -> str:
    """
    Trims text to fit platform character limits without cutting words in half.
    """
    limit = PLATFORM_LIMITS.get(platform, 2200)
    if len(text) <= limit:
        return text

    # Trim smartly at a word boundary instead of just a sentence boundary
    # This prevents cutting a word in the middle, which is more robust.
    trimmed = text[:limit]
    last_space = trimmed.rfind(" ")
    
    if last_space != -1:
        # Trim to the last full word and add an ellipsis for clarity
        return trimmed[:last_space].strip() + "..."
    else:
        # Fallback for very long single words
        return trimmed + "..."