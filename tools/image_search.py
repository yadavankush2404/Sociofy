from __future__ import annotations
import os
import random
from typing import Dict, List, Optional

import requests
from pydantic import BaseModel

UNSPLASH_API = "https://api.unsplash.com/search/photos"

class ImageResult(BaseModel):
    url: str
    author: Optional[str] = None
    link: Optional[str] = None
    alt_description: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

class UnsplashClient:
    def __init__(self, access_key: Optional[str] = None):
        """Initializes the UnsplashClient and validates the API access key."""
        self.access_key = access_key or os.getenv("UNSPLASH_ACCESS_KEY")
        # This check must be *inside* the __init__ method.
        if not self.access_key:
            raise RuntimeError("UNSPLASH_ACCESS_KEY not set. Add it to your .env file or pass it directly.")

    def search(self, query: str, per_page: int = 10) -> List[ImageResult]:
        """Performs a search against the Unsplash API."""
        params = {
            "query": query,
            "page": 1,
            "per_page": max(1, min(per_page, 30)), # Enforce API limits (1-30)
            "content_filter": "high",
            "orientation": "landscape",
        }
        headers = {"Accept-Version": "v1", "Authorization": f"Client-ID {self.access_key}"}
        
        response = requests.get(UNSPLASH_API, params=params, headers=headers, timeout=20)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        results = []
        for item in data.get("results", []):
            user = item.get("user", {})
            links = item.get("links", {})
            urls = item.get("urls", {})
            
            results.append(
                ImageResult(
                    url=urls.get("regular"),
                    author=user.get("name"),
                    link=links.get("html"),
                    alt_description=item.get("alt_description"),
                    width=item.get("width"),
                    height=item.get("height"),
                )
            )
        return results

    def best_image(self, keywords: List[str], fallback_query: str = "") -> Optional[ImageResult]:
        """
        Tries multiple queries to find the best matching image.
        It searches for the combined keywords, then each individual keyword.
        """
        # Create a unique, ordered list of search queries
        queries = list(dict.fromkeys([" ".join(keywords), *keywords, fallback_query]))
        
        for q in filter(None, queries): # filter(None, ...) removes empty strings
            try:
                hits = self.search(q, per_page=12)
                if hits:
                    # Pick a random image from the top results for variety
                    return random.choice(hits)
            except requests.RequestException:
                # If a query fails, just try the next one
                continue
                
        return None