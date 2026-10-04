import socket
import threading

from protocol import pack_message, recv_message


# Коды операций
OP_CREATE_PARTICIPANT = 1
OP_GET_PARTICIPANTS = 2
OP_GET_PARTICIPANT_BY_ID = 3
OP_CREATE_COMMAND = 4
OP_GET_COMMANDS = 5
OP_GET_COMMAND_BY_ID = 6
OP_CREATE_REPLY = 7
OP_GET_REPLIES = 8
OP_GET_REPLY_BY_ID = 9
OP_GET_REPLIES_WITH_PARTICIPANT = 10

# Хранилища данных (словари)
participants = {}
commands = {}
replies = {}

# Журнал
JOURNAL_FILE = 'journal.log'


def log(message: str):
    """Записывает сообщение в journal.log и выводит в консоль."""
    with open(JOURNAL_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')
    print(message)


# Функции модели слоя доступа к данным

def create_participant(ip: str, description: str) -> int:
    id = len(participants)
    participants[id] = {'ip': ip, 'description': description}
    return id


def get_participants():
    return participants


def get_participant_by_id(id: int):
    return participants.get(id)


def create_command(participant: int, description: str) -> int:
    import time
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
    import time
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


# Обработка запросов

def handle_request(opcode: int, body: dict) -> dict:
    """Выполняет операцию по коду и возвращает результат."""
    if opcode == OP_CREATE_PARTICIPANT:
        result = create_participant(body['ip'], body['description'])
    elif opcode == OP_GET_PARTICIPANTS:
        result = get_participants()
    elif opcode == OP_GET_PARTICIPANT_BY_ID:
        result = get_participant_by_id(body['id'])
    elif opcode == OP_CREATE_COMMAND:
        result = create_command(body['participant'], body['description'])
    elif opcode == OP_GET_COMMANDS:
        result = get_commands()
    elif opcode == OP_GET_COMMAND_BY_ID:
        result = get_command_by_id(body['id'])
    elif opcode == OP_CREATE_REPLY:
        result = create_reply(body['command'], body['response'])
    elif opcode == OP_GET_REPLIES:
        result = get_replies()
    elif opcode == OP_GET_REPLY_BY_ID:
        result = get_reply_by_id(body['id'])
    elif opcode == OP_GET_REPLIES_WITH_PARTICIPANT:
        result = get_replies_with_participant()
    else:
        return {'error': f'Неизвестный код операции: {opcode}'}
    
    return {'result': result}


# Сервер

def handle_client(conn, addr):
    """Обрабатывает одного клиента в отдельном потоке."""
    print(f'[Сервер] Подключён клиент: {addr}')
    try:
        while True:
            opcode, body = recv_message(conn)
            if opcode is None:
                break
            
            log(f'[Запрос] opcode={opcode}, body={body}')
            
            try:
                response_body = handle_request(opcode, body)
            except Exception as e:
                response_body = {'error': str(e)}
            
            response = pack_message(opcode, response_body)
            conn.sendall(response)
            
            log(f'[Ответ] opcode={opcode}, body={response_body}')
    except ConnectionResetError:
        pass
    finally:
        conn.close()
        print(f'[Сервер] Отключён клиент: {addr}')


def start_server(host: str = '127.0.0.1', port: int = 8000):
    """Запускает TCP-сервер."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f'[Сервер] Запущен на {host}:{port}')
    
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print('\n[Сервер] Остановлен')
    finally:
        server.close()


if __name__ == '__main__':
    start_server()