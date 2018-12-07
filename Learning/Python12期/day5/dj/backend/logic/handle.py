from backend.db.sql_api import select

def home():
    print('Welcome to home page')
    q_data = select('user', 'ddd')
    print('query res:', q_data)

def movie():
    print('Welcome to movie page')

def tv():
    print('Welcome to tv page')