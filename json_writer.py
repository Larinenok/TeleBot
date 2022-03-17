from pathlib import Path
from json_classes import QuestMessage, Answer


def main():    
    new_message = QuestMessage(image_path='', text='', Answers=[], id='')
    Answers = []
    answer = 0

    print('# Введите названия файла (id)')
    message_id = input()
    new_message.image_path = 'media/images/' + message_id + '.png'
    print('# Введите основной текст сообщения:')
    new_message.text = input()

    while True:
        answer += 1
        if (answer >= 5):
            break

        print('# Начните вводить новый ответ или оставьте пустым для продолжения:')
        user = input()
        if (user == ''):
            break
        else:
            print('Введите id куда будет перемещать этот ответ:')
            new_Answer = Answer(answer=answer, text='', id=input())
            new_Answer.text = user
            Answers.append(new_Answer)
    
    if (Answers == []):
        print('Введите основной id перехода:')
        new_message.id = input()
    else:
        new_message.Answers = Answers

    print(new_message.json(indent=2))
    print('# Сохранить? (Y/n)')
    user = input().lower()
    if (user == 'y' or user == ''):
        path = Path('media/messages/' + message_id + '.json')
        path.write_text(new_message.json(indent=2))


if __name__ == '__main__':
    main()