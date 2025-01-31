import logging
import sys

sys.path.append("./")
from src.bravo_core import Survey

logging.basicConfig(level=logging.DEBUG)


def test_get_questions_for_user(capsys):
    company_survey = Survey("Company", "ABC Inc.", "Technology")
    questions = company_survey.get_questions_for_user()

    with capsys.disabled():
        print("test_get_questions_for_user")
        for question in questions.questions:
            print("Question:", question.question)
            print("Answer Example:", question.answer_example)
            print("Recommendations for answer:", question.recommendations_for_answer)
            print("\n")

    assert len(questions.questions) == 3


def test_get_full_review_draft_for_user(capsys):
    from src.bravo_core.models import UserAnswersModel

    company_survey = Survey("Company", "ABC Inc.", "Information Technology")

    question_answers = [
        UserAnswersModel(
            question="How would you rate ABC Inc.'s IT support services?",
            answer="Good - it is still very expensive but I am happy with the service",
        ),
        UserAnswersModel(
            question="What do you think about the integration capabilities of ABC Inc.'s IT solutions?",
            answer="Very good integration between services with the same style of product and APIs",
        ),
        UserAnswersModel(
            question="How effective are Microsoft's IT security measures?",
            answer="Trusted - investments in security are visible and impact is clear",
        ),
    ]

    review = company_survey.get_full_review_draft_for_user(question_answers)

    with capsys.disabled():
        print("test_get_full_review_draft_for_user")
        print(review)

    assert len(review) > 0

def test_get_short_review_draft_for_user(capsys):
    from src.bravo_core.models import UserAnswersModel

    company_survey = Survey("Company", "ABC Inc.", "Information Technology")

    question_answers = [
        UserAnswersModel(
            question="How would you rate ABC Inc.'s IT support services?",
            answer="Good - it is still very expensive but I am happy with the service",
        ),
        UserAnswersModel(
            question="What do you think about the integration capabilities of ABC Inc.'s IT solutions?",
            answer="Very good integration between services with the same style of product and APIs",
        ),
        UserAnswersModel(
            question="How effective are Microsoft's IT security measures?",
            answer="Trusted - investments in security are visible and impact is clear",
        ),
    ]

    review = company_survey.get_short_review_draft_for_user(question_answers)

    with capsys.disabled():
        print("test_get_short_review_draft_for_user")
        print(review)

    assert len(review) > 0
    assert len(review) < 512