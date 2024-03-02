import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
AUTH_IMAGE = os.path.join(ASSETS_DIR, 'auth.png')
DB_NAME = os.path.join(BASE_DIR, 'database.db')
