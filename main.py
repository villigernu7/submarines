from manual_handler import ManualHandler
from network import ClientPlayer, ServerPlayer, BasePlayer
import socket

PORT = 15000
ADDRESS = "0.0.0.0"
CLIENT_ADDRESS = "192.168.77.69"


def init_listen_socket():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind((ADDRESS, PORT))
    listen_socket.listen(1)
    actual_socket, __ = listen_socket.accept()
    return actual_socket


def init_client_socket():
    client_address = input("What ip to connect to?\n")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind((ADDRESS, PORT))
    client_socket.connect((client_address, PORT))
    return client_socket


def main():
    player = None
    game_handler = ManualHandler
    player = int(input("are you P1 (server) or P2 (client). please input number only\n"))
    if player == 1:
        player = ServerPlayer(BasePlayer(init_listen_socket()), game_handler)
    elif player == 2:
        player = ClientPlayer(BasePlayer(init_client_socket()), game_handler)
    else:
        raise ValueError
    player.play_game()


if __name__ == "__main__":
    main()
