import socket
import threading

HOST = "localhost"
PORT = 55555
BUFFER_SIZE = 1024


class ClientUser:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.nick_name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.ip, self.port))

    @classmethod
    def get_name(cls) -> str:
        return input("Your nickname? >>> ")

    def receive_data(self):
        while True:
            try:
                message = self.sock.recv(BUFFER_SIZE).decode("utf-8")
                if message == "name":
                    self.sock.send(self.nick_name.encode("utf-8"))
                else:
                    print(message)
            except Exception as er:
                print(er.args[0])
                self.sock.close()
                return

    def send_data(self):
        while True:
            message = f"{self.nick_name}: {input('')}"
            self.sock.send(message.encode("utf-8"))

    def main_threads(self):

        receive_side = threading.Thread(target=self.receive_data)
        receive_side.start()

        send_side = threading.Thread(target=self.send_data)
        send_side.start()


if __name__ == "__main__":
    user_name = ClientUser.get_name()
    user = ClientUser(ip=HOST, port=PORT, name=user_name)
    user.connect()
    user.main_threads()


