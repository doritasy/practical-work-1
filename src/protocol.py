import json
import struct

# Размер поля "размер тела" — 5 байт
SIZE_BYTES = 5

# Размер поля "код операции" — 1 байт
OPCODE_BYTES = 1


def int_to_bytes(value: int, length: int) -> bytes:
    """Преобразует число в байты (big-endian)."""
    return value.to_bytes(length, byteorder='big')


def bytes_to_int(data: bytes) -> int:
    """Преобразует байты в число (big-endian)."""
    return int.from_bytes(data, byteorder='big')


def pack_message(opcode: int, body: dict) -> bytes:
    """
    Упаковывает сообщение по формату:
    [5 байт: размер тела] [1 байт: код операции] [N байт: JSON-тело]
    """
    json_str = json.dumps(body, ensure_ascii=False)
    json_bytes = json_str.encode('utf-8')
    
    body_size = len(json_bytes)
    size_bytes = int_to_bytes(body_size, SIZE_BYTES)
    opcode_bytes = int_to_bytes(opcode, OPCODE_BYTES)
    
    return size_bytes + opcode_bytes + json_bytes


def unpack_message(data: bytes) -> tuple:
    """
    Распаковывает сообщение. Возвращает (opcode, body).
    """
    body_size = bytes_to_int(data[:SIZE_BYTES])
    opcode = bytes_to_int(data[SIZE_BYTES:SIZE_BYTES + OPCODE_BYTES])
    
    json_bytes = data[SIZE_BYTES + OPCODE_BYTES: SIZE_BYTES + OPCODE_BYTES + body_size]
    body = json.loads(json_bytes.decode('utf-8'))
    
    return opcode, body


def recv_message(sock) -> tuple:
    """
    Читает из сокета одно полное сообщение.
    Возвращает (opcode, body) или (None, None), если соединение закрыто.
    """
    # Читаем заголовок: 5 байт (размер) + 1 байт (код операции)
    header_size = SIZE_BYTES + OPCODE_BYTES
    header = recv_all(sock, header_size)
    if header is None:
        return None, None
    
    body_size = bytes_to_int(header[:SIZE_BYTES])
    opcode = bytes_to_int(header[SIZE_BYTES:])
    
    # Читаем тело
    body_bytes = recv_all(sock, body_size)
    if body_bytes is None:
        return None, None
    
    body = json.loads(body_bytes.decode('utf-8'))
    return opcode, body


def recv_all(sock, n: int):
    """
    Читает ровно n байт из сокета.
    Возвращает None, если соединение закрыто до получения всех байт.
    """
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            return None
        data += chunk
    return data