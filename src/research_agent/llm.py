import instructor
from openai import OpenAI

from research_agent.config import settings


def get_client():
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    return instructor.from_openai(
        OpenAI(api_key=settings.gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    )