import tkinter as tk
import tkinter.ttk as ttk
import typing

from app.view.auth.login import Login
from app.view.auth.logout import Logout
from app.view.auth.register import Register
from app.view.screens.home import Home
from app.view.tools.text_input import TextInput


class Interface(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.container = ttk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.auth_login = Login(self.container)
        self.auth_register = Register(self.container)
        self.auth_logout = Logout(self.container)
        self.home = Home(self.container)

        self.auth_login.next_page.bind(
            '<ButtonRelease-1>', lambda e: self.show_auth_register()
        )
        self.auth_register.next_page.bind(
            '<ButtonRelease-1>', lambda e: self.show_auth_login()
        )
        self.auth_logout.next_page.bind(
            '<ButtonRelease-1>', lambda e: self.show_auth_login()
        )

        self.show_auth_login()
        self._apply_style()

    def _apply_style(self) -> None:
        def travel(widget: tk.Misc, font: str) -> None:
            """trick to change directly all entry font."""
            if isinstance(widget, ttk.Entry):
                widget.configure(font=font)
            for children in widget.winfo_children():
                travel(children, font)

        self.home.header.configure(style='BigFont.TLabel')
        self.auth_login.header.configure(style='BigFont.TLabel')
        self.auth_register.header.configure(style='BigFont.TLabel')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='white')
        style.configure('.', font='Consolas 14 normal')
        style.configure('BigFont.TLabel', font='Consolas 22 bold')
        travel(self, 'Arial 14 normal')

    def _clear_container(self) -> None:
        for children in self.container.winfo_children():
            children.pack_forget()

    def show_auth_login(self) -> None:
        self._clear_container()
        self.title('Login')
        self.geometry('850x400+0+0')
        self.auth_login.username.entry.focus()
        self.auth_login.pack(side='top', fill='both', expand=True)

    def show_auth_logout(self) -> None:
        self._clear_container()
        self.title('Logout')
        self.geometry('500x150')
        self.auth_logout.pack(side='top', fill='both', expand=True)

    def show_auth_register(self) -> None:
        self._clear_container()
        self.title('Register')
        self.geometry('850x550+0+0')
        self.auth_register.name.entry.focus()
        self.auth_register.pack(side='top', fill='both', expand=True)

    def show_home(self) -> None:
        self._clear_container()
        self.title('Home')
        self.geometry('800x500+0+0')
        self.home.pack(side='top', fill='both', expand=True)

    def login_feedback(self, field: str, feedback: str) -> None:
        fields: typing.Dict[str, TextInput] = {
            'username': self.auth_login.username,
            'password': self.auth_login.password,
        }
        if field in fields.keys():
            fields[field].set_feedback(feedback)
            fields[field].entry.focus()

    def register_feedback(self, field: str, feedback: str) -> None:
        fields: typing.Dict[str, TextInput] = {
            'name': self.auth_register.name,
            'email': self.auth_register.email,
            'username': self.auth_register.username,
            'password': self.auth_register.password,
        }
        if field in fields.keys():
            fields[field].set_feedback(feedback)
            fields[field].entry.focus()

    def login_form(self) -> typing.Tuple[str, str]:
        username = self.auth_login.username.text()
        password = self.auth_login.password.text()
        return (username, password)

    def register_form(self) -> typing.Tuple[str, str, str, str]:
        name = self.auth_register.name.text()
        email = self.auth_register.email.text()
        username = self.auth_register.username.text()
        password = self.auth_register.password.text()
        return (name, email, username, password)

    def clear_login_form(self) -> None:
        self.auth_login.username.set_text('')
        self.auth_login.password.set_text('')

    def clear_register_form(self) -> None:
        self.auth_register.name.set_text('')
        self.auth_register.email.set_text('')
        self.auth_register.username.set_text('')
        self.auth_register.password.set_text('')

    def clear_login_feedback(self) -> None:
        self.auth_login.username.set_feedback('')
        self.auth_login.password.set_feedback('')

    def clear_register_feedback(self) -> None:
        self.auth_register.name.set_feedback('')
        self.auth_register.email.set_feedback('')
        self.auth_register.username.set_feedback('')
        self.auth_register.password.set_feedback('')

    @property
    def login_button(self) -> ttk.Button:
        return self.auth_login.button

    @property
    def register_button(self) -> ttk.Button:
        return self.auth_register.button

    @property
    def logout_button(self) -> ttk.Button:
        return self.home.logout_button
