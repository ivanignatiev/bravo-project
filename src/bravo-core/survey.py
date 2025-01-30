import logging
from clients.ollama import llm
from schemas.survey_questions import SurveyQuestionsList
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

class Survey:
    organization_name: str
    industry: str
    
    def __init__(self, organization_name: str, industry: str) -> None:
        self.organization_name = organization_name
        self.industry = industry

    def get_user_questions(self) -> str:
        """Get most important questions to help create positive and useful review."""

        parser = PydanticOutputParser(pydantic_object=SurveyQuestionsList)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant that assist user for creating a positive and helpful for others review for organization {organization_name} in industry {industry}.",
                ),
                ("human", "List 3 most important question which will require very short answers to help create a positive and useful review. {format_instructions}"),
            ]
        ).partial(
            format_instructions=parser.get_format_instructions()
        )
        
        logging.debug(f"Prompt: {prompt}")

        chain = prompt | llm | parser

        return chain.invoke(
            {
                "organization_name": self.organization_name,
                "industry": self.industry,
            }
        )