# Sociofy (Streamlit + Unsplash)

Generate platform-optimized captions and fetch matching royalty-free images in seconds.

## Features
- CrewAI multi-agent pipeline: Content Strategist (caption) + Image Researcher (keywords)
- Unsplash API integration with fallback queries
- Multi-platform styles (Instagram, Twitter/X, LinkedIn)
- Tone control + optional hashtags
- History (SQLite) and downloads (.txt, .zip)
- Single-command launch via Streamlit


## Env
- `OPENAI_API_KEY` — from OpenAI
- `UNSPLASH_ACCESS_KEY` — create on unsplash.com/developers
- Optional: `OPENAI_MODEL` (default `gpt-4o-mini`), `TEMPERATURE`, `MAX_TOKENS`

## Notes
- Respect Unsplash guidelines. Credit is displayed when available.
- For production, consider rate limit handling + caching.
