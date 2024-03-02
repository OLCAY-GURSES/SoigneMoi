import sqlite3
from tkinter.messagebox import showinfo

from app.model import Model
from app.view.interface import Interface


class Controller:
    def __init__(self, db_name: str) -> None:
        self.interface = Interface()
        self.model = Model(db_name)

        self.interface.login_button.configure(command=self.login)
        self.interface.register_button.configure(command=self.register)
        self.interface.logout_button.configure(command=self.logout)

    def start(self) -> None:
        self.interface.mainloop()

    def login(self) -> None:
        username, password = self.interface.login_form()
        self.interface.clear_login_feedback()

        if username == '':
            self.interface.login_feedback('username', 'Required field.')
        if password == '':
            self.interface.login_feedback('password', 'Required field.')

        if username and password:
            finded = self.model.select_user_to_login(username, password)
            if not finded:
                self.interface.login_feedback(
                    'username', 'username or password incorrect.'
                )
            else:
                self.interface.clear_register_feedback()
                self.interface.clear_login_form()
                self.interface.clear_register_form()
                self.interface.show_home()

    def register(self) -> None:
        name, email, username, password = self.interface.register_form()

        try:
            self.interface.clear_register_feedback()
            self.model.insert_user(name, email, username, password)
        except sqlite3.DatabaseError:
            if name == '':
                self.interface.register_feedback('name', 'Required field.')

            if self.model.select_user_by_email(email):
                self.interface.register_feedback(
                    'email', 'Email already registered.'
                )

            if username == '':
                self.interface.register_feedback('username', 'Required field.')

            elif self.model.select_user_by_username(username):
                self.interface.register_feedback(
                    'username', 'User already registered.'
                )

            if password == '':
                self.interface.register_feedback('password', 'Required field.')
        else:
            self.interface.clear_login_feedback()
            self.interface.clear_login_form()
            self.interface.clear_register_form()
            self.interface.show_home()
            showinfo('Success', f'User {username} created.')

    def logout(self) -> None:
        self.interface.show_auth_logout()
