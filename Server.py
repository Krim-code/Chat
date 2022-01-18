import socket
import threading
import time
import sqlite3
import hashlib


# функция отвечающая за хеширование:

def hashpassword(mystring):
# Предположительно по умолчанию UTF-8
    hash_object = hashlib.md5(mystring.encode())
    return hash_object.hexdigest()


# окно логики регистрации для сервера
class Registration_Server_Logical():
    # Creating socket
    def __init__(self):
        super().__init__()
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.server.bind(
            ("127.0.0.1", 9099)
        )

    # принимаем входящее подключение и получаем данные от пользователя
    def receive_registration_user(self):
        while True:
            user_socket, address = self.server.accept()

            # выводим ip пользователя
            print(f"User {user_socket} connected!")

            # получаем информацию от пользователя на сервер
            data_login = user_socket.recv(2048)
            data_login = data_login.decode("utf-8")
            print(data_login)
            data_password = user_socket.recv(2048)
            data_password = data_password.decode("utf-8")
            print(data_password)
            data_password = hashpassword(data_password)
            user_socket.send(self.some_logical_registation(data_login, data_password).encode("utf-8"))

    # listen server
    def listen_registration_part_server(self):
        self.server.listen(0)
        print("Server is listening")
        # получаем логин и пароль с помощью потоков
        receive_login_pass = threading.Thread(target=self.receive_registration_user)
        receive_login_pass.start()

    # логика регистрации(чек логина и пароля на индивидуальность и сама регистрация)
    def some_logical_registation(self, user_login, user_password):
        db = sqlite3.connect('server.db')
        sql = db.cursor()

        sql.execute("""CREATE TABLE IF NOT EXISTS useri (
            login TEXT,
            password TEXT,
            cash BIGINT
        )""")

        db.commit()

        sql.execute(f"SELECT login FROM useri WHERE login = '{user_login}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO useri VAlUES (?, ?, ?)", (user_login, user_password, 0))
            db.commit()
            return 'Зарегистрировано'

        else:
            return 'Такая запись уже есть'


# окно логики авторизации для сервера
class Authorization_Server_Logical:
    # Creating socket
    def __init__(self):
        super().__init__()
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.server.bind(
            ("127.0.0.1", 9098)
        )

    # принимаем входящее подключение и получаем данные от пользователя

    # listen server
    def listen_authorization_part_server(self):
        self.server.listen(0)
        print("Server is listening_Too")
        threading.Thread(target=self.receive_authorization_data).start()

    # принимаем входящее подключение
    def receive_authorization_data(self):
        while True:
            user_socket, address = self.server.accept()
            # выводим ip пользователя
            print(f"User {user_socket} connected!")

            # получаем информацию от пользователя на сервер
            authoriz_login = user_socket.recv(2048)
            authoriz_password = user_socket.recv(2048)
            authoriz_login = authoriz_login.decode("utf-8")
            authoriz_password = authoriz_password.decode("utf-8")
            # анализируем логин и пароль юзера
            authoriz_password = hashpassword(authoriz_password)
            check = self.logical_part_authorization(authoriz_login, authoriz_password)
            user_socket.send(check.encode("utf-8"))

    def logical_part_authorization(self, verif_login, verif_pass):
        db = sqlite3.connect('server.db')
        sql = db.cursor()
        db.commit()

        sql.execute(f"SELECT login FROM useri WHERE login = '{verif_login}' AND password = '{verif_pass}'")
        if sql.fetchone() is None:

            return "Пароль или логин не верны"
        else:
            return "Успех"


class Chat_logical_Server():
    def __init__(self):
        self.nick = []
        self.clients = {}
        self.addresses = {}

        self.SERVER = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.SERVER.bind(
            ("127.0.0.1", 9045)
        )

    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            self.client, client_address = self.SERVER.accept()
            print(f"{client_address} has connected.")
            self.addresses[self.client] = client_address
            threading.Thread(target=self.handle_client, args=(self.client,)).start()

    def handle_client(self, client):  # Takes client socket as argument.
        """Handles a single client connection."""

        name = client.recv(2048).decode("utf8")
        self.nick.append(str(name))
        print(self.nick)
        client.send(bytes(" ".join(self.nick) + "<><>!<><>", "utf8"))
        self.broadcast(bytes(" ".join(self.nick) + "<><>!<><>", "utf8"))
        msg = "%s has joined the chat!" % name
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name

        while True:
            msg = client.recv(2048)
            if msg != bytes("{quit}", "utf8"):
                self.broadcast(msg, name + ": ")
            else:
                # client.send(bytes("{quit}", "utf8"))
                client.close()
                del self.clients[client]
                self.nick.remove(name)
                self.broadcast(bytes("%s has left the chat." % name, "utf8"))
                self.broadcast(bytes(" ".join(self.nick) + "<><>!<><>", "utf8"))
                break

    def broadcast(self, msg, prefix=""):  # prefix is for name identification.
        """Broadcasts a message to all the clients."""
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)

    def listening(self):
        self.SERVER.listen(0)
        print("Waiting for connection...")
        ACCEPT_THREAD = threading.Thread(target=self.accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.SERVER.close()


#
#
reg = Registration_Server_Logical()
registration_server = threading.Thread(target=reg.listen_registration_part_server)
registration_server.start()

authoriz = Authorization_Server_Logical()
authorization_server = threading.Thread(target=authoriz.listen_authorization_part_server())
authorization_server.start()

chat = Chat_logical_Server()
cht = threading.Thread(target=chat.listening())
cht.start()
