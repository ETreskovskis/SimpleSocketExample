import socket
import threading
from dataclasses import dataclass
from typing import List, Tuple

HOST = "localhost"
PORT = 55555
BUFFER_SIZE = 1024


@dataclass(init=False)
class Clients:
    all_clients: List[Tuple]


class ChatServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.ask_name = "name"
        self.welcome_msg = "{} has joined the chat room!"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _start_server(self):
        self.sock.bind((self.ip, self.port))
        self.sock.listen()

    @staticmethod
    def broadcast_info(message: str):
        encode_msg = message.encode("utf-8")
        for client, name in Clients.all_clients:
            client.send(encode_msg)

    def remove_client(self, client):
        for num, clients in enumerate(Clients.all_clients):
            if client in clients:
                Clients.all_clients.pop(num)
                client.close()
                _, name = client
                msg = f"Client >> {name} has lef the char room..."
                self.broadcast_info(msg)

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(BUFFER_SIZE)
                self.broadcast_info(message)
            except Exception as er:
                print(er)
            finally:
                self.remove_client(client)
                return

    def main_loop(self):
        self._start_server()

        while True:
            print(f"Starting server and listening to {self.ip}:{self.port}")
            client, address = self.sock.accept()
            print(f"Connection established with {str(address)}")
            client.send(self.ask_name.encode("utf-8"))
            client_name = client.recv(BUFFER_SIZE)
            Clients.all_clients.append((client, client_name))
            msg = self.welcome_msg.format(client_name)
            self.broadcast_info(message=msg)
            client.send("You connected to the chat room!".encode("utf-8"))
            # start threads here
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


if __name__ == "__main__":
    server = ChatServer(HOST, PORT)
    server.main_loop()
