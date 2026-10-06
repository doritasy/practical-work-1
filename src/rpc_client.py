import socket

from protocol import pack_message, recv_message


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


class RpcClient:
    """Клиент для удалённого вызова процедур по TCP."""

    def __init__(self, host: str = '127.0.0.1', port: int = 8000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def close(self):
        self.sock.close()

    def _call(self, opcode: int, body: dict):
        """Отправляет запрос и получает ответ."""
        request = pack_message(opcode, body)
        self.sock.sendall(request)
        _, response_body = recv_message(self.sock)
        if 'error' in response_body:
            raise Exception(response_body['error'])
        return response_body['result']

    def create_participant(self, ip: str, description: str) -> int:
        return self._call(
            OP_CREATE_PARTICIPANT,
            {'ip': ip, 'description': description}
        )

    def get_participants(self):
        return self._call(OP_GET_PARTICIPANTS, {})

    def get_participant_by_id(self, id: int):
        return self._call(OP_GET_PARTICIPANT_BY_ID, {'id': id})

    def create_command(self, participant: int, description: str) -> int:
        return self._call(
            OP_CREATE_COMMAND,
            {'participant': participant, 'description': description}
        )

    def get_commands(self):
        return self._call(OP_GET_COMMANDS, {})

    def get_command_by_id(self, id: int):
        return self._call(OP_GET_COMMAND_BY_ID, {'id': id})

    def create_reply(self, command: int, response: str) -> int:
        return self._call(
            OP_CREATE_REPLY,
            {'command': command, 'response': response}
        )

    def get_replies(self):
        return self._call(OP_GET_REPLIES, {})

    def get_reply_by_id(self, id: int):
        return self._call(OP_GET_REPLY_BY_ID, {'id': id})

    def get_replies_with_participant(self):
        return self._call(OP_GET_REPLIES_WITH_PARTICIPANT, {})

    def reset(self):
        return self._call(99, {})
