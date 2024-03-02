from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk


class Home(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configure(padding=15)

        # header
        header_container = ttk.Frame(self)
        header_container.pack(side='top', fill='x')

        self.header = ttk.Label(header_container)
        self.header.configure(text='Welcome')
        self.header.configure(anchor='center')
        self.header.pack(side='top', fill='x')

        # center_container
        center_container = ttk.Frame(self)
        center_container.pack(side='top', fill='both', expand=True)

        # footer
        footer_container = ttk.Frame(self)
        footer_container.pack(side='bottom', fill='x')

        self.date_time_var = tk.StringVar()
        label_date_time = ttk.Label(footer_container)
        label_date_time.configure(textvariable=self.date_time_var)
        label_date_time.pack(side='right')
        self._update_date_time()

        self.logout_button = ttk.Button(footer_container)
        self.logout_button.configure(text='Logout')
        self.logout_button.pack(side='right', padx=5)

    def _update_date_time(self) -> None:
        now = datetime.now()
        date = now.strftime('%Y/%m/%d')
        time = now.strftime('%H:%M:%S')
        self.date_time_var.set(f'{date} {time}')
        self.after(1000, self._update_date_time)
