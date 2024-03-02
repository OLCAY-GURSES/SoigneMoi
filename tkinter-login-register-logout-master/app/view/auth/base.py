import tkinter as tk
import tkinter.ttk as ttk
from app import constants


class Base(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.left = ttk.Frame(self)
        self.left.configure(padding=15)
        self.left.pack(side='left', fill='both', expand=True)

        self.right = ttk.Frame(self)
        self.right.configure(padding=15)
        self.right.pack(side='right', fill='x', expand=True)

        self.image = tk.PhotoImage(file=constants.AUTH_IMAGE)
        label_image = ttk.Label(self.left)
        label_image.configure(image=self.image)
        label_image.configure(anchor='center')
        label_image.pack(side='top', fill='both', expand=True)

        self.header = ttk.Label(self.right)
        self.header.configure(text='Auth')
        self.header.configure(anchor='center')
        self.header.pack(side='top', fill='x', expand=True, pady=15)
