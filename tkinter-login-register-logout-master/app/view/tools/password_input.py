from app.view.tools.text_input import TextInput


class PasswordInput(TextInput):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.entry.configure(show='*')
