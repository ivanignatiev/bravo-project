import logging
from typing import List
from .clients.ollama import llm
from .schemas.survey_questions import SurveyQuestionsList
from .models import UserAnswersModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)

MAX_LLM_REQUEST_RETRIES = 3


class Survey:
    type: str
    name: str
    industry: str

    def __init__(self, type: str, name: str, industry: str) -> None:
        """
        Parameters
        ----------
        type : str
            Type of target for review.
            Person, Organization, Product, Service, etc.
        name : str
            Name of target for review.
        industry : str
            Industry of target for review.
        """

        self.type = type
        self.name = name
        self.industry = industry

    def get_questions_for_user(self) -> str:
        """
        Get TOP 3 most important questions to help create positive and useful review.
        """
        logger.info("Getting questions for.")

        parser = PydanticOutputParser(pydantic_object=SurveyQuestionsList)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Role: You are a helpful assistant that assist user for creating review for {type} {name} in industry {industry}."
                    ),
                ),
                (
                    "human",
                    (
                        "Request: List 3 most important questions and answer recommendations which will require very short answers from me to help create a review."
                        "Your questions and recommendations must help me write a short and specific review which must highlight most important elements for {industry}, contain constructive feedback, be positive and contain helpful information for others."
                        "\n"
                        "Result: {format_instructions}"
                    ),
                ),
            ]
        ).partial(format_instructions=parser.get_format_instructions())

        chain = prompt | llm | parser

        retry = 0
        while retry < MAX_LLM_REQUEST_RETRIES:
            try:
                return chain.invoke(
                    {
                        "type": self.type,
                        "name": self.name,
                        "industry": self.industry,
                    }
                )
            except Exception as e:
                logger.error(f"Error getting questions: {e}. Retrying.")
                retry += 1

    def get_full_review_draft_for_user(
        self, questions_answers: List[UserAnswersModel]
    ) -> str:
        history = [
            (
                "system",
                (
                    "Role: You are a helpful assistant that assist user for creating review for {type} {name} in industry {industry}."
                ),
            )
        ]

        for question_answer in questions_answers:
            history.append(
                ("ai", f"Question: {question_answer.question}"),
            )
            history.append(
                ("human", question_answer.answer),
            )

        history.append(
            (
                "human",
                (
                    "Based on my answers to your questions, write a specific review which must highlight most important elements for {industry}, contain constructive feedback, be positive and contain helpful information for others."
                    "\n"
                ),
            )
        )

        prompt = ChatPromptTemplate.from_messages(history)

        chain = prompt | llm

        retry = 0
        while retry < MAX_LLM_REQUEST_RETRIES:
            try:
                response = chain.invoke(
                    {
                        "type": self.type,
                        "name": self.name,
                        "industry": self.industry,
                    }
                )
                
                return response.content
            except Exception as e:
                logger.error(f"Error getting questions: {e}. Retrying.")
                retry += 1


    def get_short_review_draft_for_user(
        self, questions_answers: List[UserAnswersModel]
    ) -> str:
        history = [
            (
                "system",
                (
                    "Role: You are a helpful assistant that assist user for creating review for {type} {name} in industry {industry}."
                ),
            )
        ]

        for question_answer in questions_answers:
            history.append(
                ("ai", f"Question: {question_answer.question}"),
            )
            history.append(
                ("human", question_answer.answer),
            )

        history.append(
            (
                "human",
                (
                    "Based on my answers to your questions, write a short specific review which must highlight most important elements for {industry}, contain constructive feedback, be positive and contain helpful information for others."
                    "Review must be 512 characters length or less."
                    "\n"
                ),
            )
        )

        prompt = ChatPromptTemplate.from_messages(history)

        chain = prompt | llm

        retry = 0
        while retry < MAX_LLM_REQUEST_RETRIES:
            try:
                response = chain.invoke(
                    {
                        "type": self.type,
                        "name": self.name,
                        "industry": self.industry,
                    }
                )
                
                return response.content
            except Exception as e:
                logger.error(f"Error getting questions: {e}. Retrying.")
                retry += 1
