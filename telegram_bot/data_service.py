import psycopg2
from config import database_password
import datetime


 

def make_cursor():
    conn = psycopg2.connect(database="FinantialBot", host="localhost", user="postgres", password=database_password, port=5432)
    cursor = conn.cursor()
    return cursor

def add_user(user_id, create_date):
    cursor = make_cursor()
    query = "insert into chat (select %(p_user_id)s, %(p_create_date)s where not exists ( select 1 from chat where chat_id = '%(p_user_id)s'));"
    cursor.execute(query,{'p_user_id' : user_id, 'p_create_date' : create_date})
    cursor.connection.commit()
    cursor.close()
    cursor.connection.close()
    
# if __name__ == '__main__':
#     add_user(1, datetime.datetime.now())








