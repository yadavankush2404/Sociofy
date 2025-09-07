# crew/crew.py
from __future__ import annotations
from crewai import Crew, Process
from .agents import Content_Strategist_Agent, Image_Search_Agent
from .tasks import CaptionTask, KeywordTask


def build_crew():
    # Bind agents to tasks dynamically to keep tasks reusable
    caption_task = CaptionTask.model_copy(update={"agent": Content_Strategist_Agent})
    keyword_task = KeywordTask.model_copy(update={
                                        "agent": Image_Search_Agent,
                                        'context': [caption_task]
                                    })

    return Crew(
        agents=[Content_Strategist_Agent, Image_Search_Agent],
        tasks=[caption_task, keyword_task],
        process="sequential",
        output_log_file="logs/logs.json",
        verbose=True,
    )