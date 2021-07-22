import socket
import threading
from utils import Config, Logger


class ChatServer:
    def __init__(self, ip: str, port: int):
        self.clients = list()
        self.ip = ip
        self.port = port
        self.ask_name = "name"
        self.welcome_msg = "{} has joined the chat room!"
        self.instruction = "To quit the chat room >> !quit"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _start_server(self):
        self.sock.bind((self.ip, self.port))
        self.sock.listen()

    def broadcast_info(self, message: bytes):
        for client, _ in self.clients:
            client.send(message)

    def remove_client(self, client):
        for num, clients in enumerate(self.clients):
            if client in clients:
                self.clients.pop(num)
                _, name = clients
                msg = f"Client >> {name.decode('utf-8')} has lef the chat room..."
                Logger.info(msg)
                self.broadcast_info(msg.encode("utf-8"))
                client.close()

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(Config.BUFFER_SIZE)
                if message:
                    Logger.info(message.decode("utf-8"))
                elif message and message.decode("utf-8").split(":")[-1].strip() == "!quit":
                    print(message)
                    print(message.decode("utf-8").split(":")[-1].strip())
                    self.remove_client(client)

                self.broadcast_info(message)
            except Exception as er:
                Logger.error(er.args[0])
                self.remove_client(client)
                return

    def main_loop(self):
        self._start_server()

        while True:
            print(f"Starting server and listening to {self.ip}:{self.port}")
            client, address = self.sock.accept()
            Logger.info(f"Connection established with {str(address)}")
            print(f"Connection established with {str(address)}")
            client.send(self.ask_name.encode("utf-8"))
            client_name = client.recv(Config.BUFFER_SIZE)

            Logger.info(f"New user: {address}, nickname: {client_name}")
            self.clients.append((client, client_name))
            msg = self.welcome_msg.format(client_name).encode("utf-8")
            self.broadcast_info(message=msg)
            client.send(f"\nYou connected to the chat room! {self.instruction}".encode("utf-8"))
            # start threads here
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


if __name__ == "__main__":
    Logger(filename="server_logger")
    server = ChatServer(Config.HOST, Config.PORT)
    server.main_loop()
