import dataclasses

@dataclasses.dataclass
class UserAnswersModel:
    question: str
    answer: str
    
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer