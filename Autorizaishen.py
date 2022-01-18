import sqlite3

db = sqlite3.connect('server.db')
sql = db.cursor()
db.commit()

user_login = input('Login: ')
user_password = input('Password: ')

sql.execute(f"SELECT login FROM useri WHERE login = '{user_login}' AND password = '{user_password}'")
if sql.fetchone() is None:

    print("Пароль или логин не верны")
else:
    print('Welcome')