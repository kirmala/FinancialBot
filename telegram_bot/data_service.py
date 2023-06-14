import psycopg2
from config import database_password
import datetime
import uuid


def make_cursor():
    conn = psycopg2.connect(database="FinantialBot", host="localhost", user="postgres", password=database_password, port=5432)
    cursor = conn.cursor()
    return cursor

def add_user(user_id, create_date):
    cursor = make_cursor()
    query = "INSERT INTO chat (chat_id, create_date) SELECT %(p_user_id)s, %(p_create_date)s WHERE NOT EXISTS (SELECT 1 from chat WHERE chat_id = %(p_user_id)s);"
    cursor.execute(query,{'p_user_id' : user_id, 'p_create_date' : create_date})
    cursor.connection.commit()
    cursor.close()
    cursor.connection.close()

def add_check(check_fn, check_fd, check_fpd, chat_id, check_ofd, check_place, check_sum, check_date):
    check_id = str(uuid.uuid4())
    cursor = make_cursor()
    query = """ 
    INSERT INTO "check" (check_id, check_fn, check_fd, check_fpd, chat_id, check_ofd, check_place, check_sum, check_date)
    SELECT %(p_check_id)s, %(p_check_fn)s, %(p_check_fd)s, %(p_check_fpd)s, %(p_chat_id)s, %(p_check_ofd)s, %(p_check_place)s, %(p_check_sum)s, %(p_check_date)s
    WHERE NOT EXISTS (
        SELECT 1 FROM "check" WHERE check_fn = %(p_check_fn)s OR check_fd = %(p_check_fd)s OR check_fpd = %(p_check_fpd)s
    );
    """
    cursor.execute(query,{'p_check_id' : check_id, 'p_check_fn': check_fn, 'p_check_fd' : check_fd, 'p_check_fpd' : check_fpd, 'p_chat_id' : chat_id, 'p_check_ofd' : check_ofd, 'p_check_place': check_place, 'p_check_sum': check_sum, 'p_check_date' : check_date})
    cursor.connection.commit()
    cursor.close()
    cursor.connection.close()

    
# if __name__ == '__main__':
#     add_user(1, datetime.datetime.now())








