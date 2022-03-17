from pydantic import BaseModel


class Answer(BaseModel):
    answer: str
    text: str
    id: str


class QuestMessage(BaseModel):
    image_path: str
    text: str
    Answers: list[Answer]
    id: str