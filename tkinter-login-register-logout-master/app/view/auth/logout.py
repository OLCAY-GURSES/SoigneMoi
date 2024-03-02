import tkinter.ttk as ttk


class Logout(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.next_page = ttk.Label(self)
        self.next_page.configure(
            text='You have disconected, login again \u27a4'
        )
        self.next_page.configure(anchor='center')
        self.next_page.configure(cursor='hand2')
        self.next_page.pack(expand=True)
