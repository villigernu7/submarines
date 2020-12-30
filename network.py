import socket
import packets
import exceptions
import random


class BasePlayer:

    def __init__(self, connection_socket: socket.socket):
        self.socket = connection_socket

    def send_guess(self, row, column):
        packet = packets.ATTACK_HEADER + chr(row) + chr(column)
        response = self.send_and_receive(packet)
        if not self.validate_packet(response, packets.RESPONSE_HEADER):
            self.sudden_close(exceptions.GameFlowException())
        if ord(response[-1]) > packets.Result.DEFEAT.value:
            self.sudden_close(exceptions.IllegalArgumentException())
        return ord(response[-1])

    def recv_attack(self):
        attack = self.socket.recv(1024).decode()
        if not self.validate_packet(attack, packets.ATTACK_HEADER):
            self.sudden_close(exceptions.GameFlowException)
        return ord(attack[-2]), ord(attack[-1])

    def send_result(self, result):
        packet = packets.RESPONSE_HEADER + chr(result)
        self.socket.send(packet.encode())

    def sudden_close(self, exception):
        self.socket.send(packets.STOP_GAME.encode())
        self.socket.close()
        raise exception

    def send_and_receive(self, packet):
        self.socket.send(packet.encode())
        return self.socket.recv(1024).decode()

    def end_game(self):
        self.socket.close()

    def play_game(self, is_starting_player: bool, game_handler):
        try:
            is_my_turn = is_starting_player
            result = 0
            while result != packets.Result.DEFEAT:
                if is_my_turn:
                    row, col = game_handler.get_guess()
                    result = self.send_guess(row, col)
                    if result == 0:
                        is_my_turn = not is_my_turn
                    game_handler.set_result(row, col, result)
                else:
                    row, col = self.recv_attack()
                    result = game_handler.get_result(row, col)
                    if result == 0:
                        is_my_turn = not is_my_turn
                    self.send_result(result)
        finally:
            self.end_game()
            raise

    @staticmethod
    def validate_packet(response, packet_header):
        if len(response) == 0:
            raise ConnectionError
        return (response.startswith(packet_header)) and (ord(response[0]) == len(response[1:]))


class ClientPlayer:

    def __init__(self, base_player: BasePlayer, game_handler):
        self.base_player = base_player
        self.game_handler = game_handler

    def initiate_game(self):
        response = self.base_player.send_and_receive(packets.REQUEST_START_GAME)
        if not self.base_player.validate_packet(response, packets.CONFIRM_START_GAME):
            self.base_player.sudden_close(exceptions.StartGameException())

    def signal_ready(self):
        response = self.base_player.send_and_receive(packets.READY_CLIENT_PLAYER)
        if not self.base_player.validate_packet(response, packets.READY_SERVER_PLAYER_HEADER):
            self.base_player.sudden_close(exceptions.GameFlowException())
        starting_player = response[-1]
        if starting_player == packets.StartingPlayer.SERVER_PLAYER.value:
            return False
        elif starting_player == packets.StartingPlayer.CLIENT_PLAYER.value:
            return True
        else:
            self.base_player.sudden_close(exceptions.IllegalArgumentException())

    def play_game(self):
        self.initiate_game()
        is_my_turn = self.signal_ready()
        self.base_player.play_game(is_my_turn, self.game_handler)


class ServerPlayer:

    def __init__(self, base_player: BasePlayer, game_handler):
        self.base_player = base_player
        self.game_handler = game_handler

    def initiate_game(self):
        response = self.base_player.socket.recv(1024).decode()
        if not self.base_player.validate_packet(response, packets.REQUEST_START_GAME):
            self.base_player.sudden_close(exceptions.StartGameException())
        self.base_player.socket.send(packets.CONFIRM_START_GAME.encode())

    def signal_ready(self):
        response = self.base_player.socket.recv(1024).decode()
        if not self.base_player.validate_packet(response, packets.READY_CLIENT_PLAYER):
            self.base_player.sudden_close(exceptions.GameFlowException())
        starting_player = chr(random.randint(2, 3))
        packet = packets.READY_SERVER_PLAYER_HEADER + starting_player
        self.base_player.socket.send(packet.encode())
        if starting_player == packets.StartingPlayer.SERVER_PLAYER.value:
            return True
        elif starting_player == packets.StartingPlayer.CLIENT_PLAYER.value:
            return False
        else:
            self.base_player.sudden_close(exceptions.IllegalArgumentException())

    def play_game(self):
        self.initiate_game()
        is_my_turn = self.signal_ready()
        self.base_player.play_game(is_my_turn, self.game_handler)
