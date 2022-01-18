import socket
import threading
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
import base64

#функции кодирования сообщений

def encoded_messege(sample_string):
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("utf-8")
    return base64_string

def decoded_messege(base64_string):
    base64_bytes = base64_string.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string

# окно авторизации
class GUI:
    def __init__(self):
        self.incorrect_clock = 0

    def authorization(self):

        # функция проверки авторизации пользователя
        def autorization_check():

            if len(login_input.get()) and len(password_input.get()) != 0:
                il = str(login_input.get())
                inp = str(password_input.get())
                autoriz = Authorization_Client_Logical()
                data, login = autoriz.receive_data_about_authorization_user(il, inp)
                if data == "Успех":
                    closed_root()
                    Chat_forms(login)
                else:
                    self.incorrect_clock += 1
                    messagebox.showinfo("Введите логин и пароль!", "Вы ввели некорректные данные!")
                    if self.incorrect_clock == 5:
                        closed_root()



            else:
                messagebox.showinfo("Введите логин и пароль!", "Введите логин и пароль!")

        # функция закрытия окна
        def closed_root():
            root.destroy()

        # функция запускающая окно регистрации
        def registr():
            closed_root()
            Registraition_forms.invite_registr_forms(self)

        root = tk.Tk()
        root.title("Security Chat")
        root.config(bg="black")
        root.geometry("510x530")

        # logo
        logo = ImageTk.PhotoImage(Image.open("img\logo.png"))
        logotipe = tk.Label(root, image=logo, bg="black")
        logotipe.grid(row=1, column=1)

        # instruction
        instruction = tk.Label(text="Authorization", font="Raleway", fg="white", bg="black")
        instruction.grid(row=0, column=1, padx=10, pady=20)
        instruction = tk.Label(text="Please input login and password", font="Raleway", fg="white", bg="black")
        instruction.grid(row=2, column=1, padx=10, pady=20)

        # login and password input
        login = tk.StringVar()
        login_input = tk.Entry(textvariable=login, bg="pink", width=45)
        login_lable = tk.Label(text="Login:", font="Raleway", fg="white", bg="black")
        login_lable.grid(row=3, column=0, padx=10, pady=10)
        login_input.grid(row=3, column=1, padx=10, pady=20)

        password = tk.StringVar()
        password_input = tk.Entry(textvariable=password, width=45)
        password_lable = tk.Label(text="Password:", font="Raleway", fg="white", bg="black")
        password_lable.grid(row=4, column=0, padx=10, pady=10)
        password_input.grid(row=4, column=1, pady=10)

        # button
        input_button = tk.Button(text="Input", width=38, bg="#ba1ace", command=autorization_check)
        input_button.grid(row=5, column=1, pady=20)

        registration_button = tk.Button(text="Registration", width=38, bg="#ba1ace", command=registr)
        registration_button.grid(row=6, column=1, pady=0)

        root.mainloop()


# окно регистрации
class Registraition_forms:

    def invite_registr_forms(self):
        # функция создания окна индикации регистрации
        def indicate_registration(ind):
            if ind:
                messagebox.showinfo('Поздравляем!', 'Зарегистрировано')
                back_to_authorization()
            else:
                messagebox.showinfo('Ошибка!', 'Такая запись уже есть')

        # функция кнопки регистрации
        def registration_user():
            if len(reg_login.get()) and len(reg_password.get()) != 0:
                rl = str(reg_login.get())
                rp = str(reg_password.get())
                reg = Registration_Client_Logical()
                indicate = reg.receive_data_about_reg_user(rl, rp)
                indicate_registration(indicate)
            else:
                messagebox.showinfo("Введите логин и пароль!", "Введите логин и пароль!")

        # функция закрытия окна регистрации
        def closed_registr_forms():
            reg.destroy()

        # функция возвращающая окно входа
        def back_to_authorization():
            closed_registr_forms()
            GUI.authorization(self)

        reg = tk.Tk()
        reg.title("Security Chat")
        reg.config(bg="black")
        reg.geometry("600x530")

        # logo
        logo = ImageTk.PhotoImage(Image.open("img/reg.png"))
        logotipe = tk.Label(reg, image=logo, bg="black")
        logotipe.grid(row=1, column=1)

        # instruction
        instruction = tk.Label(text="Registration", font="Raleway", fg="white", bg="black")
        instruction.grid(row=0, column=1, padx=10, pady=20)
        instruction = tk.Label(text="Please input login and password", font="Raleway", fg="white", bg="black")
        instruction.grid(row=2, column=1, padx=10, pady=20)

        # login and password input
        reg_login = tk.StringVar()
        login_input = tk.Entry(textvariable=reg_login, bg="pink", width=45)
        login_lable = tk.Label(text="Login:", font="Raleway", fg="white", bg="black")
        login_lable.grid(row=3, column=0, padx=10, pady=10)
        login_input.grid(row=3, column=1, padx=10, pady=20)

        reg_password = tk.StringVar()
        password_input = tk.Entry(textvariable=reg_password, width=45)
        password_lable = tk.Label(text="Password:", font="Raleway", fg="white", bg="black")
        password_lable.grid(row=4, column=0, padx=10, pady=10)
        password_input.grid(row=4, column=1, pady=10)

        # button
        input_button = tk.Button(text="Back to authorization", width=38, bg="#ba1ace", command=back_to_authorization)
        input_button.grid(row=5, column=1, pady=20)

        registration_button = tk.Button(text="Registration", width=38, bg="#ba1ace", command=registration_user)
        registration_button.grid(row=6, column=1, pady=0)

        reg.mainloop()


# окно логики регистрации для клиента
class Registration_Client_Logical:
    # Creating socket
    def __init__(self):
        self.client = socket.socket(

            socket.AF_INET,
            socket.SOCK_STREAM

        )
        # connecting client on server
        self.client.connect(

            ("127.0.0.1", 9099)

        )

    # получаем информацию от сервера
    def receive_data_about_reg_user(self, a, b):
        # функция проверки попытки регистрации
        def check_registration_process(data):
            if data == 'Зарегистрировано':
                return True
            if data == 'Такая запись уже есть':
                return False

        # функция отправляющая логин
        def send_reg_login(a):
            self.client.send((a).encode("utf-8"))

        # функция отправляющая пароль
        def send_reg_pass(b):
            self.client.send((b).encode("utf-8"))

        # отправка логина и пароля в два потока
        send_login = threading.Thread(target=send_reg_login, args=(a,))
        send_login.start()
        send_pass = threading.Thread(target=send_reg_pass, args=(b,))
        send_pass.start()
        data = self.client.recv(2048)
        data = data.decode("utf-8")
        print(data)
        output = check_registration_process(data)

        # функция завершения процесса регистрации и вывода сообщения
        if output:
            self.client.close()
            return True
        else:
            return False


# окно логики авторизации для клиента
class Authorization_Client_Logical:
    def __init__(self):
        self.client = socket.socket(

            socket.AF_INET,
            socket.SOCK_STREAM

        )
        # connecting client on server
        self.client.connect(

            ("127.0.0.1", 9098)

        )

    def receive_data_about_authorization_user(self, authorization_login, authorization_password):
        # функция отправляющая логин
        def send_authorization_login(a):
            self.client.send((a).encode("utf-8"))

        # функция отправляющая пароль
        def send_authorization_pass(b):
            self.client.send((b).encode("utf-8"))

        # получаем информацию от сервера
        # отправка логина и пароля в два потока
        send_login = threading.Thread(target=send_authorization_login, args=(authorization_login,))
        send_login.start()
        send_pass = threading.Thread(target=send_authorization_pass, args=(authorization_password,))
        send_pass.start()
        data = self.client.recv(2048).decode("utf-8")
        print(data)
        return data, authorization_login


# окно чата(формы)
class Chat_forms():
    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = self.clients_socket.recv(2048).decode("utf8")
                if "<><>!<><>" not in msg:
                    self.msg_list.insert(tk.END, msg)

                else:
                    msg =msg.replace("<><>!<><>","")
                    self.clients = msg.split()
                    print(self.clients)
                    self.update_online()




            except OSError:  # Possibly client has left the chat.
                break
    def update_online(self):
        self.online_list.delete(0,tk.END)
        for client in self.clients:
            self.online_list.insert(tk.END, client)




    def send(self):
        """Handles sending of messages."""
        msg = self.my_msg.get()
        self.my_msg.set("")# Clears input field.
        self.clients_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.clients_socket.close()
            self.chat_root.destroy()

    def on_closing(self):
        """This function is to be called when the window is closed."""
        self.my_msg.set("{quit}")
        self.send()

    def __init__(self, name):

        self.clients = []
        self.name = name

        self.addresses = {}

        self.clients_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.clients_socket.connect(
            ("127.0.0.1", 9045)
        )

        # создаём окно чата
        self.chat_root = tk.Tk()
        self.chat_root.title("Krim_Chat")
        self.chat_root.config(bg="black")
        self.chat_root.geometry('700x670')
        self.chat_root.resizable(width=False,height=False)
        self.chat_root.columnconfigure([0, 1], minsize=100)
        self.chat_root.rowconfigure([0, 1,2], minsize=0)

        messages_frame = tk.Frame(self.chat_root)
        self.my_msg = tk.StringVar()  # For the messages to be sent.
        self.my_msg.set("Type your messages here.")
        scrollbar = tk.Scrollbar(messages_frame)  # To navigate through past messages.

        # Following will contain the messages.
        self.msg_list = tk.Listbox(messages_frame, height=24, width=45, yscrollcommand=scrollbar.set, fg="white",
                                   bg="black",font="Raleway 13")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.msg_list.pack()
        messages_frame.grid(row=1, column=0)

        online_frame = tk.Frame(self.chat_root)
        scrollbar_online = tk.Scrollbar(online_frame)  # To navigate for online user
        self.online_list = tk.Listbox(online_frame, height=24, width=20, yscrollcommand=scrollbar_online.set, fg="#ba1ace",
                                   bg="black" ,font="Raleway 13", )
        scrollbar_online.pack(side=tk.RIGHT, fill=tk.Y)
        self.online_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.online_list.pack()
        online_frame.grid(row=1, column=1 ,pady = 20)


        entry_field = tk.Entry(self.chat_root, textvariable=self.my_msg, width=58)
        entry_field.grid(row=2, column=0, sticky="w")
        send_button = tk.Button(self.chat_root, text="Send", command=self.send, width=10, fg="white", bg="#ba1ace")
        send_button.grid(row=2, column=0, sticky="e")

        # online
        # logo
        logo1 = ImageTk.PhotoImage(Image.open("img/logo.png"))
        logotipe1 = tk.Label(self.chat_root, image=logo1, bg="black", width=308)
        logotipe1.grid(row=0, column=0, sticky="nw")

        logo = ImageTk.PhotoImage(Image.open("img/online.png"))
        logotipe = tk.Label(self.chat_root, image=logo, bg="black", width=220)
        logotipe.grid(row=0, column=1, sticky="nw", padx=30)

        self.chat_root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.clients_socket.send(bytes(self.name, "utf8"))
        threading.Thread(target=self.receive).start()
        # вызываем окно чата
        self.chat_root.mainloop()

#
# chat = Chat_forms("kiss")

# reg = Registration_Client_Logical()
# # reg.receive_data_about_reg_user("мамкаёб", "15век фокс презент")
gui = GUI()
gui.authorization()
# autoriz = Authorization_Client_Logical()
# autoriz.receive_data_about_authorization_user("fff","fff")
