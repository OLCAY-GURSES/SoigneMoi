from app import constants
from app.controller import Controller


if __name__ == '__main__':
    app_controller = Controller(constants.DB_NAME)
    app_controller.start()
