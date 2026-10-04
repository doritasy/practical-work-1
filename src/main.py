import time

participants = {}
commands = {}
replies = {}

#1 и 2 задание
def create_participant(ip: str, description: str) -> int:
    id = len(participants)
    participants[id] = {'ip': ip, 'description': description}
    return id

def get_participants():
    return participants

def get_participant_by_id(id: int):
    return participants.get(id)

def create_command(participant: int, description: str) -> int:
    id = len(commands)
    commands[id] = {
        'participant': participant,
        'created': int(time.time()),
        'description': description
    }
    return id

def get_commands():
    return commands

def get_command_by_id(id: int):
    return commands.get(id)

def create_reply(command: int, response: str) -> int:
    id = len(replies)
    replies[id] = {
        'command': command,
        'response': response
    }
    return id

def get_replies():
    return replies

def get_reply_by_id(id: int):
    return replies.get(id)

#3 задание
def get_replies_with_participant():
    result = []
    now = int(time.time())
    for reply in replies.values():
        # Находим команду по ссылке из ответа
        command = commands.get(reply['command'])
        if command is None:
            continue
        # Проверяем условие по времени
        if command['created'] < now - 8 * 60:
            continue
        # Находим участника по ссылке из команды
        participant = participants.get(command['participant'])
        if participant is None:
            continue
        result.append({
            'description': command['description'],
            'ip': participant['ip'],
            'response': reply['response']
        })
    return result

#4 и 5 задание
def repl():
    while True:
        try:
            user_command = input()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход")
            break

        match user_command:
            case 'create_participant':
                ip = input()
                description = input()
                print(create_participant(ip, description))
            case 'get_participants':
                print(get_participants())
            case 'get_participant_by_id':
                try:
                    id = int(input())
                except ValueError:
                    print("Ошибка: id должен быть числом")
                    continue
                result = get_participant_by_id(id)
                if result is None:
                    print("Участник не найден")
                else:
                    print(result)
            case 'create_command':
                try:
                    participant = int(input())
                except ValueError:
                    print("Ошибка: id участника должен быть числом")
                    continue
                if get_participant_by_id(participant) is None:
                    print("Ошибка: участник не найден")
                    continue
                description = input()
                print(create_command(participant, description))
            case 'get_commands':
                print(get_commands())
            case 'get_command_by_id':
                try:
                    id = int(input())
                except ValueError:
                    print("Ошибка: id должен быть числом")
                    continue
                result = get_command_by_id(id)
                if result is None:
                    print("Команда не найдена")
                else:
                    print(result)
            case 'create_reply':
                try:
                    command = int(input())
                except ValueError:
                    print("Ошибка: id команды должен быть числом")
                    continue
                if get_command_by_id(command) is None:
                    print("Ошибка: команда не найдена")
                    continue
                response = input()
                print(create_reply(command, response))
            case 'get_replies':
                print(get_replies())
            case 'get_reply_by_id':
                try:
                    id = int(input())
                except ValueError:
                    print("Ошибка: id должен быть числом")
                    continue
                result = get_reply_by_id(id)
                if result is None:
                    print("Ответ не найден")
                else:
                    print(result)
            case 'get_replies_with_participant': #3 задание
                print(get_replies_with_participant())
            case 'Выход':
                break
            case _:
                print("Неизвестная команда")

repl()

    
