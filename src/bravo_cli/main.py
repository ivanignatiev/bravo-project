import sys
sys.path.append('./')

import click
from rich.console import Console
from rich.markdown import Markdown
from typing import List
from src.bravo_core import Survey
from src.bravo_core.models import UserAnswersModel
from tools.loading import loading_animation

def get_user_input(survey: Survey) -> List[UserAnswersModel]:

    with loading_animation("Getting question for user to create a review"):
        questions = survey.get_questions_for_user()

    user_question_answers : List[UserAnswersModel] = []

    click.echo(
        click.style(
            "Here are the top 3 most important questions to help you create a positive and useful review:",
            fg="green",
        )
    )
    for question in questions.questions:
        click.secho(question.question, fg="yellow")
        click.secho("Answer Example:" + " " + question.answer_example, fg="white")
        click.secho(
            "Recommendations for answer:" + " " + question.recommendations_for_answer,
            fg="white",
        )
        answer = click.prompt(click.style("Your answer", fg="yellow"), type=str)
        user_question_answers.append(
            UserAnswersModel(question=question.question, answer=answer)
        )
        click.echo("\n")

    return user_question_answers

def create_and_print_review(survey: Survey, user_question_answers: List[UserAnswersModel]) -> None:

    with loading_animation("Creating a draft for complete review"):
        review = survey.get_full_review_draft_for_user(user_question_answers)

    click.echo(
        click.style(
            ("Here is your full review proposition for the target:" "\n"),
            fg="green",
        )
    )

    console = Console()
    md = Markdown(review)
    console.print(md)

    with loading_animation("Creating a short version of the review"):
        review = survey.get_short_review_draft_for_user(user_question_answers)

    click.echo(
        click.style(
            ("Here is your short review proposition for the target:" "\n"),
            fg="green",
        )
    )

    console = Console()
    md = Markdown(review)
    console.print(md)
    
    click.echo(
        click.style(
            ("\nThank you for using Bravo!\n"),
            fg="green",
        )
    )

def main():
    click.echo("Bravo project helps you to write a review for any target. Please provide a basic information about your review target to start:")
    type = click.prompt(
        click.style(
            "Type of your target for review (Person, Company, Product, Service)",
            fg="yellow",
        ),
        prompt_suffix="?",
        type=str,
    )
    name = click.prompt(
        click.style("Name of the target for review", fg="yellow"),
        prompt_suffix="?",
        type=str,
    )
    industry = click.prompt(
        click.style("Industry of the target for review", fg="yellow"),
        prompt_suffix="?",
        type=str,
    )
    
    survey = Survey(type, name, industry)

    user_question_answers = get_user_input(survey)

    create_and_print_review(survey, user_question_answers)


if __name__ == "__main__":
    main()
