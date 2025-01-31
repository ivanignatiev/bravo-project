from typing import List
from pydantic import BaseModel, Field


class SurveyQuestion(BaseModel):
    """
    Structure for survey question with its answer examples and recommendations for writing.
    """

    question: str = Field(..., title="Question", description="Survey question.")
    answer_example: str = Field(
        ...,
        title="Answer Example",
        description=(
            "Positive answer example to the survey question."
            "answer must be short and specific, highlight most important elements for the industry, contain constructive feedback, be positive and contain helpful information for others."
        ),
    )
    recommendations_for_answer: str = Field(
        ...,
        title="Recommendations for writing answer on the survey question",
        description="Recommendations how to write an answer on the survey question.",
    )


class SurveyQuestionsList(BaseModel):
    """
    Structure with list of 3 most important survey questions with answer examples and recommendations for writing.
    """

    questions: List[SurveyQuestion] = Field(
        ...,
        title="Questions",
        description="List of survey questions with answer examples and recommendations for writing.",
    )
