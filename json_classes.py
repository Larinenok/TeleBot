from pydantic import BaseModel


class Answer(BaseModel):
    answer: str
    text: str
    id: str
    is_true: bool


class QuestMessage(BaseModel):
    image_path: str
    text: str
    Answers: list[Answer]
    id: str
    total_questions: int
