import hypothesis.strategies as st
from hypothesis import settings
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
from rpc_client import RpcClient


class RpcServerModel(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.client = RpcClient('127.0.0.1', 8000)
        self.client.reset()

        self.model_participants = {}
        self.model_commands = {}
        self.model_replies = {}

        self.next_participant_id = 0
        self.next_command_id = 0
        self.next_reply_id = 0

    def teardown(self):
        self.client.close()

    # PARTICIPANT
    @rule(ip=st.text(min_size=1), description=st.text(min_size=1))
    def create_participant(self, ip, description):
        pid = self.client.create_participant(ip, description)
        assert pid == self.next_participant_id

        # Ключ — строка, потому что JSON возвращает строковые ключи
        self.model_participants[str(pid)] = {
            'ip': ip, 'description': description}
        self.next_participant_id += 1

    @rule()
    def get_participants(self):
        server_data = self.client.get_participants()
        assert server_data == self.model_participants

    @rule(pid=st.integers(min_value=0, max_value=100))
    def get_participant_by_id(self, pid):
        server_data = self.client.get_participant_by_id(pid)
        assert server_data == self.model_participants.get(str(pid))

    # COMMAND
    @rule(participant=st.integers(min_value=0, max_value=100),
          description=st.text(min_size=1))
    def create_command(self, participant, description):
        cid = self.client.create_command(participant, description)
        assert cid == self.next_command_id

        self.model_commands[str(cid)] = {
            'participant': participant,
            'description': description
        }
        self.next_command_id += 1

    @rule()
    def get_commands(self):
        server_data = self.client.get_commands()
        assert server_data.keys() == self.model_commands.keys()
        for cid in server_data:
            server_participant = server_data[cid]['participant']
            model_participant = self.model_commands[cid]['participant']
            assert server_participant == model_participant

            server_description = server_data[cid]['description']
            model_description = self.model_commands[cid]['description']
            assert server_description == model_description

    @rule(cid=st.integers(min_value=0, max_value=100))
    def get_command_by_id(self, cid):
        server_data = self.client.get_command_by_id(cid)
        if str(cid) in self.model_commands:
            assert server_data is not None
            assert server_data['participant'] == self.model_commands[str(
                cid)]['participant']
            assert server_data['description'] == self.model_commands[str(
                cid)]['description']
        else:
            assert server_data is None

    # REPLY
    @rule(command=st.integers(min_value=0, max_value=100),
          response=st.text(min_size=1))
    def create_reply(self, command, response):
        rid = self.client.create_reply(command, response)
        assert rid == self.next_reply_id

        self.model_replies[str(rid)] = {
            'command': command, 'response': response}
        self.next_reply_id += 1

    @rule()
    def get_replies(self):
        server_data = self.client.get_replies()
        assert server_data == self.model_replies

    @rule(rid=st.integers(min_value=0, max_value=100))
    def get_reply_by_id(self, rid):
        server_data = self.client.get_reply_by_id(rid)
        assert server_data == self.model_replies.get(str(rid))

    # СЛОЖНЫЙ ЗАПРОС
    @rule()
    def complex_query(self):
        server_result = self.client.get_replies_with_participant()

        model_result = []
        for rid, reply in self.model_replies.items():
            command = self.model_commands.get(str(reply['command']))
            if command is None:
                continue
            participant = self.model_participants.get(
                str(command['participant']))
            if participant is None:
                continue
            model_result.append({
                'description': command['description'],
                'ip': participant['ip'],
                'response': reply['response']
            })

        assert len(server_result) == len(model_result)
        for item in model_result:
            assert item in server_result

    # ИНВАРИАНТ
    @invariant()
    def sizes_agree(self):
        assert len(
            self.model_participants) == len(
            self.client.get_participants())
        assert len(self.model_commands) == len(self.client.get_commands())
        assert len(self.model_replies) == len(self.client.get_replies())


TestRpcServer = RpcServerModel.TestCase
TestRpcServer.settings = settings(max_examples=20, stateful_step_count=15)
