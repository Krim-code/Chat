import sqlite3

db = sqlite3.connect('server.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS useri (
    login TEXT,
    password TEXT,
    cash BIGINT
)""")

db.commit()

user_login = input('Login: ')
user_password = input('Password: ')

sql.execute(f"SELECT login FROM useri WHERE login = '{user_login}'")
if sql.fetchone() is None:
    sql.execute(f"INSERT INTO useri VAlUES (?, ?, ?)", (user_login, user_password, 0))
    db.commit()
    print('Зарегистрировано')
else:
    print('Такая запись уже есть')

    for value in sql.execute("SELECT * FROM useri"):
        print(value)

 