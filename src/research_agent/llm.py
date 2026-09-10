import os

import instructor
from dotenv import load_dotenv
from openai import OpenAI
from research_agent.config import settings

load_dotenv()

client = instructor.from_openai(
    OpenAI(
        api_key=settings.openai_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
)
