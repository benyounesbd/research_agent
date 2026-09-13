import instructor
from openai import OpenAI

from research_agent.config import settings


def get_client():
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    return instructor.from_openai(
        OpenAI(api_key=settings.openai_api_key)
    )