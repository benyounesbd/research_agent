import instructor
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = instructor.from_openai(
    OpenAI()
)