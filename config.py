from init import get_enviroment_variable


HOST = get_enviroment_variable("HOST")
DATABASE = get_enviroment_variable("DATABASE")
PORT = get_enviroment_variable("PORT")
USER = get_enviroment_variable("USER")
PASSWORD = get_enviroment_variable("PASSWORD")

DICT_TABLES = [
    'genres',
    'platforms',
    'publishers',
    'languages'
]