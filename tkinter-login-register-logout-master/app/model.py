import sqlite3
import typing


class Model:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name

        with sqlite3.connect(self.db_name) as conn:
            sql = """
                create table if not exists user (
                iduser integer primary key autoincrement,
                name text not null,
                email text unique,
                username text unique,
                password text not null)
                """
            conn.execute(sql)

    def insert_user(
        self, name: str, email: str, username: str, password: str
    ) -> int:
        formatted_name = name.strip() or None
        formatted_email = email.strip() or None
        formatted_username = username.strip() or None
        formatted_password = password.strip() or None

        with sqlite3.connect(self.db_name) as conn:
            sql = 'insert into user (name, email, username, password) values (?, ?, ?, ?)'
            parameters = (
                formatted_name,
                formatted_email,
                formatted_username,
                formatted_password,
            )
            cursor = conn.execute(sql, parameters)
            return cursor.lastrowid

    def select_user_by_username(
        self, username: str
    ) -> typing.List[typing.Tuple]:
        formatted_username = username.strip() or None

        with sqlite3.connect(self.db_name) as conn:
            sql = 'select iduser, name, email, username, email from user where username = ?'
            parameters = (formatted_username,)
            cursor = conn.execute(sql, parameters)
            return cursor.fetchall()

    def select_user_by_email(self, email: str) -> typing.List[typing.Tuple]:
        formatted_email = email.strip() or None

        with sqlite3.connect(self.db_name) as conn:
            sql = 'select iduser, name, email, username, email from user where email = ?'
            parameters = (formatted_email,)
            cursor = conn.execute(sql, parameters)
            return cursor.fetchall()

    def select_user_to_login(
        self, username: str, password: str
    ) -> typing.Optional[typing.Tuple]:
        formatted_usertname = username.strip() or None
        formatted_password = password.strip() or None

        with sqlite3.connect(self.db_name) as conn:
            sql = 'select iduser, name, email, username, email from user where username = ? and password = ?'
            parameters = (formatted_usertname, formatted_password)
            cursor = conn.execute(sql, parameters)
            return cursor.fetchone()
