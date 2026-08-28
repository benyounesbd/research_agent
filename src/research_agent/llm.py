import os

import instructor
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = instructor.from_openai(
    OpenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
)
