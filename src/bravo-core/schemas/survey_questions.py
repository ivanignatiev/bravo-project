from typing import List
from pydantic import BaseModel, Field

class SurveyQuestion(BaseModel):
    """
    Survey question with response example.
    Question will require very short answers to help create a positive and useful review for organization.
    """
    question: str = Field(..., title="Question", description="Survey question.")
    response_example: str = Field(..., title="Response Example", description="Response example to the survey question.")

class SurveyQuestionsList(BaseModel):
    """ 
    List 3 most important questions with response example.
    Questions will require very short answers to help create a positive and useful review for organization.
    """
    questions: List[SurveyQuestion] = Field(..., title="Questions", description="List of survey questions with response example.")
    