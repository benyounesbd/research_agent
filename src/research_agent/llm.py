
import instructor
from openai import OpenAI

from research_agent.config import settings

client = instructor.from_openai(
    OpenAI(
        api_key=settings.openai_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
)
