from rpc_client import RpcClient


def main():
    client = RpcClient('127.0.0.1', 8000)
    print('Подключено к серверу\n')

    print('Участники')
    pid1 = client.create_participant('192.168.1.1', 'Сервер')
    print(f'Создан участник id={pid1}')
    pid2 = client.create_participant('10.0.0.1', 'Клиент')
    print(f'Создан участник id={pid2}')

    print(f'Все участники: {client.get_participants()}')
    print(f'Участник 0: {client.get_participant_by_id(0)}')
    print()

    print('Команды')
    cid1 = client.create_command(pid1, 'Проверить статус')
    print(f'Создана команда id={cid1}')
    cid2 = client.create_command(pid2, 'Отправить данные')
    print(f'Создана команда id={cid2}')

    print(f'Все команды: {client.get_commands()}')
    print(f'Команда 0: {client.get_command_by_id(0)}')
    print()

    print('Ответы')
    rid1 = client.create_reply(cid1, 'Всё работает')
    print(f'Создан ответ id={rid1}')
    rid2 = client.create_reply(cid2, 'Данные отправлены')
    print(f'Создан ответ id={rid2}')

    print(f'Все ответы: {client.get_replies()}')
    print(f'Ответ 0: {client.get_reply_by_id(0)}')
    print()

    print('Сложный запрос')
    result = client.get_replies_with_participant()
    for item in result:
        print(f'  {item}')

    client.close()
    print('\nСоединение закрыто')


if __name__ == '__main__':
    main()