"""
Модель слоя доступа к данным.

Реализованы операции для трёх сущностей: Participant, Command, Reply.
Содержит функцию repl() — интерактивный режим.
"""

import time

participants = {}
commands = {}
replies = {}


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


def get_replies_with_participant():
    result = []
    now = int(time.time())
    for reply in replies.values():
        command = commands.get(reply['command'])
        if command is None:
            continue
        if command['created'] < now - 8 * 60:
            continue
        participant = participants.get(command['participant'])
        if participant is None:
            continue
        result.append({
            'description': command['description'],
            'ip': participant['ip'],
            'response': reply['response']
        })
    return result


def cmd_create_participant():
    ip = input()
    description = input()
    print(create_participant(ip, description))


def cmd_get_participants():
    print(get_participants())


def cmd_get_participant_by_id():
    try:
        id = int(input())
    except ValueError:
        print("Ошибка: id должен быть числом")
        return
    result = get_participant_by_id(id)
    if result is None:
        print("Участник не найден")
    else:
        print(result)


def cmd_create_command():
    try:
        participant = int(input())
    except ValueError:
        print("Ошибка: id участника должен быть числом")
        return
    if get_participant_by_id(participant) is None:
        print("Ошибка: участник не найден")
        return
    description = input()
    print(create_command(participant, description))


def cmd_get_commands():
    print(get_commands())


def cmd_get_command_by_id():
    try:
        id = int(input())
    except ValueError:
        print("Ошибка: id должен быть числом")
        return
    result = get_command_by_id(id)
    if result is None:
        print("Команда не найдена")
    else:
        print(result)


def cmd_create_reply():
    try:
        command = int(input())
    except ValueError:
        print("Ошибка: id команды должен быть числом")
        return
    if get_command_by_id(command) is None:
        print("Ошибка: команда не найдена")
        return
    response = input()
    print(create_reply(command, response))


def cmd_get_replies():
    print(get_replies())


def cmd_get_reply_by_id():
    try:
        id = int(input())
    except ValueError:
        print("Ошибка: id должен быть числом")
        return
    result = get_reply_by_id(id)
    if result is None:
        print("Ответ не найден")
    else:
        print(result)


def cmd_get_replies_with_participant():
    print(get_replies_with_participant())


def repl():
    handlers = {
        'create_participant': cmd_create_participant,
        'get_participants': cmd_get_participants,
        'get_participant_by_id': cmd_get_participant_by_id,
        'create_command': cmd_create_command,
        'get_commands': cmd_get_commands,
        'get_command_by_id': cmd_get_command_by_id,
        'create_reply': cmd_create_reply,
        'get_replies': cmd_get_replies,
        'get_reply_by_id': cmd_get_reply_by_id,
        'get_replies_with_participant': cmd_get_replies_with_participant,
    }

    while True:
        try:
            user_command = input()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход")
            break

        if user_command == 'Выход':
            break

        handler = handlers.get(user_command)
        if handler is None:
            print("Неизвестная команда")
        else:
            handler()


repl()
