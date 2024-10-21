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

def add_receipt(receipt_fn, receipt_fd, receipt_fpd, chat_id, receipt_ofd, receipt_place, receipt_sum, receipt_date, receipt_id):
    cursor = make_cursor()
    query = """ 
    INSERT INTO receipt (receipt_id, receipt_fn, receipt_fd, receipt_fpd, chat_id, receipt_ofd, receipt_place, receipt_sum, receipt_date)
    SELECT %(p_receipt_id)s, %(p_receipt_fn)s, %(p_receipt_fd)s, %(p_receipt_fpd)s, %(p_chat_id)s, %(p_receipt_ofd)s, %(p_receipt_place)s, %(p_receipt_sum)s, %(p_receipt_date)s;
    """
    cursor.execute(query,{'p_receipt_id' : receipt_id, 'p_receipt_fn': receipt_fn, 'p_receipt_fd' : receipt_fd, 'p_receipt_fpd' : receipt_fpd, 'p_chat_id' : chat_id, 'p_receipt_ofd' : receipt_ofd, 'p_receipt_place': receipt_place, 'p_receipt_sum': receipt_sum, 'p_receipt_date' : receipt_date})
    cursor.connection.commit()
    cursor.close()
    cursor.connection.close()

def find_receipt(receipt_fn, receipt_fd, receipt_fpd):
    cursor = make_cursor()
    query = """ SELECT 1 FROM receipt WHERE receipt_fn = %(p_receipt_fn)s OR receipt_fd = %(p_receipt_fd)s OR receipt_fpd = %(p_receipt_fpd)s """
    cursor.execute(query,{'p_receipt_fn': receipt_fn, 'p_receipt_fd' : receipt_fd, 'p_receipt_fpd' : receipt_fpd})
    exist = cursor.fetchall()
    if (len(exist) == 0):
        return False
    return True
    

def add_items(name, price, amount, sum, receipt_id):
    item_id = str(uuid.uuid4())
    cursor = make_cursor()
    query = """
    INSERT INTO receipt_item (item_name, item_price, item_amount, item_sum, item_id, receipt_id)
    SELECT %(p_item_name)s, %(p_item_price)s, %(p_item_amount)s, %(p_item_sum)s, %(p_item_id)s, %(p_receipt_id)s
    """
    cursor.execute(query,{'p_item_name' : name, 'p_item_price': price, 'p_item_amount' : amount, 'p_item_sum' : sum, 'p_item_id' : item_id, 'p_receipt_id' : receipt_id})
    cursor.connection.commit()
    cursor.close()
    cursor.connection.close()

def delete_user(user_id):
    cursor = make_cursor()
    query = """
    DELETE FROM chat WHERE chat_id = %(p_user_id)s
    """
    cursor.execute(query,{'p_user_id' : user_id})
    cursor.connection.commit()
    cursor.close()
    cursor.connection.close()


    
# if __name__ == '__main__':
#     add_user(1, datetime.datetime.now())








