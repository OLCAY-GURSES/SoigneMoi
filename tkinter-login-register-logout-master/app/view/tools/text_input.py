import tkinter as tk
import tkinter.ttk as ttk


class TextInput(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label_var = tk.StringVar()
        self.label = ttk.Label(self)
        self.label.configure(textvariable=self.label_var)
        self.label.configure(anchor='center')
        self.label.pack(side='top', fill='x')

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self)
        self.entry.configure(textvariable=self.entry_var)
        self.entry.configure(justify='center')
        self.entry.pack(side='top', fill='x')

        self.feedback_var = tk.StringVar()
        self.feedback = ttk.Label(self)
        self.feedback.configure(textvariable=self.feedback_var)
        self.feedback.configure(anchor='center')
        self.feedback.configure(foreground='red')
        self.feedback.pack(side='top', fill='x')

    def description(self) -> str:
        return self.label_var.get()

    def set_description(self, description: str) -> None:
        self.label_var.set(description)

    def text(self) -> str:
        return self.entry_var.get()

    def set_text(self, text: str) -> None:
        self.entry_var.set(text)

    def feedback(self) -> str:
        return self.feedback_var.get()

    def set_feedback(self, feedback: str) -> None:
        self.feedback_var.set(feedback)
