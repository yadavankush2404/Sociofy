# crew/tasks.py
from __future__ import annotations
from crewai import Task

caption_system_prompt = (
    "You will write a short, catchy caption optimized for the given platform and tone. "
    "Include a concise hook, value, and (optional) CTA. Use tasteful emojis. Keep within platform limits."
    )

image_system_prompt = "From the provided caption, list 4-8 concise image search keywords that best represent the visual theme. \
        Return ONLY a comma-separated list of keywords, no extra text."


CaptionTask = Task(
    description= "Write a platform-optimized caption for the topic: '{topic}'.\n \
    Platform: {platform}. Tone: {tone}. Include hashtags if 'include_hashtags' is true.",
    expected_output= "A single caption string that is ready to post (no surrounding quotes).",
    agent=None, # set by crew assembly
    async_execution=False,
    )

KeywordTask = Task(
     #description= "Give comma-separated keywords extracted from the result of CaptionTask agent generated caption, extract image keywords. Return ONLY comma-separated keywords.", # adding {caption} in description and then adding context to captionTask agent did not work why?
     #"Analyze the {platform} caption generated in the context from the previous task CaptionTask.\n\n "
     description = (  "Using the caption output generated from the previous task for {platform} platform\n\n "
                     "Based *only* on that caption, extract 5-7 relevant keywords that would be perfect for finding a matching image. "
                     "Focus on the main themes."
                     "Return ONLY a comma-separated list of keywords."
                ),
    expected_output="Comma-separated keywords, 4-8 items.",
    agent=None, # set by crew assembly
    async_execution=False,
    context = None # set by crew assembly
    )