from pathlib import Path
from json_classes import QuestMessage, Variant


def main():    
    new_message = QuestMessage(image_path='', text='', variants=[])
    variants = []
    variant_id = 0

    print('# Введите названия файла (id)')
    message_id = input()
    new_message.image_path = 'media/images/' + message_id + '.png'
    print('# Введите основной текст сообщения:')
    new_message.text = input()

    while True:
        variant_id += 1
        if (variant_id >= 5):
            break

        print('# Начните вводить новый ответ или оставьте пустым для продолжения')
        user = input()
        if (user == ''):
            break
        else:
            new_variant = Variant(id=variant_id, text='')
            new_variant.text = user
            variants.append(new_variant)
    new_message.variants = variants

    print(new_message.json())
    print('# Сохранить? (Y/n)')
    user = input().lower()
    if (user == 'y' or user == ''):
        path = Path('media/messages/' + message_id + '.json')
        path.write_text(new_message.json(indent=2))


if __name__ == "__main__":
    main()