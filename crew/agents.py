# crew/agents.py
from __future__ import annotations
import os
from crewai import Agent
from langchain_openai import ChatOpenAI

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "400"))

llm = ChatOpenAI(model=OPENAI_MODEL, temperature=TEMPERATURE, max_tokens=MAX_TOKENS)

Content_Strategist_Agent = Agent(
    role="Content Strategist",
    goal= "Draft catchy, platform-aware, on-brand social media captions that drive engagement. and include a smooth call-to-action when appropriate.",
    backstory= "You are a senior social media copywriter. You know tone, hooks, CTA, emoji etiquette, and platform limits (Twitter 280, Instagram 2200, LinkedIn 3000).",
    allow_delegation=False,
    llm=llm,
)

Image_Search_Agent = Agent(
    role="Image Researcher",
    goal="Extract key visual themes from the caption and find a relevant, high-quality, royalty-free image on Unsplash.",
    backstory="You are a creative researcher with an eye for compelling, brand-safe visuals.",
    allow_delegation=False,
    llm=llm,
)