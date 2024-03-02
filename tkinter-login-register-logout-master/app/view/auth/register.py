import tkinter.ttk as ttk
from app.view.auth.base import Base
from app.view.tools.text_input import TextInput
from app.view.tools.password_input import PasswordInput


class Register(Base):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.header.configure(text='Register')

        self.name = TextInput(self.right)
        self.name.set_description('Name')
        self.name.pack(side='top', fill='x', expand=True)

        self.email = TextInput(self.right)
        self.email.set_description('Email')
        self.email.pack(side='top', fill='x', expand=True)

        self.username = TextInput(self.right)
        self.username.set_description('Username')
        self.username.pack(side='top', fill='x', expand=True)

        self.password = PasswordInput(self.right)
        self.password.set_description('Password')
        self.password.pack(side='top', fill='x', expand=True)

        self.button = ttk.Button(self.right)
        self.button.configure(text='Register')
        self.button.pack(side='top', fill='x', expand=True, pady=15)

        self.next_page = ttk.Label(self.right)
        self.next_page.configure(text='Already have an account? Login \u27a4')
        self.next_page.configure(anchor='center')
        self.next_page.configure(cursor='hand2')
        self.next_page.pack(side='top', fill='x', expand=True)
