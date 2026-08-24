from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    sub_questions: list[str] = Field(
        min_length=1,
        description="Questions that need to be answered during the research",
    )
    search_queries: list[str] = Field(
        min_length=1,
        description="Search queries to use for researching the topic",
    )


class Source(BaseModel):
    title: str
    url: str
    content: str