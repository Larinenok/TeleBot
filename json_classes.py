from pydantic import BaseModel


class Variant(BaseModel):
    id: int
    text: str


class QuestMessage(BaseModel):
    image_path: str
    text: str
    variants: list[Variant]