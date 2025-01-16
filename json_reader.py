from pathlib import Path
from json_classes import QuestMessage


def load_message_by_id(id: str):
    path = Path('media/messages/' + id + '.json')
    quest_message = QuestMessage.parse_file(path)
    return quest_message

def get_quizes() -> list:
    path = Path('media/messages')
    files = [f.name.replace('.json', '') for f in path.iterdir() if f.is_file()]

    return files


def main():
    # id = 'example'
    # path = Path('media/messages/' + id + '.json')
    # quest_message = QuestMessage.parse_file(path)
    # print(quest_message.json(indent=2))
    # print(quest_message.text)
    # print(quest_message.image_path)
    print(get_quizes())


if __name__ == '__main__':
    main()
