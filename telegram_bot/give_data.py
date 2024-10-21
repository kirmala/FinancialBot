import psycopg2
from config import database_password
import uuid
import csv
path = 'C:\python\best_project'


def make_cursor():
    conn = psycopg2.connect(database="FinantialBot", host="localhost", user="postgres", password=database_password, port=5432)
    cursor = conn.cursor()
    return cursor

def save_binary_to_file(sql_data, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        header = ['receipt_place', 'receipt_date', 'item_name', 'item_price', 'item_amount', 'item_sum']
        writer.writerow(header)
        writer.writerows(sql_data)


def give_all_data(user_id):
    cursor = make_cursor()
    query = """
    SELECT r.receipt_place, r.receipt_date, ri.item_name, ri.item_price, ri.item_amount, ri.item_sum
    FROM receipt as r
    JOIN receipt_item AS ri ON r.receipt_id = ri.receipt_id
    where r.chat_id = %(p_user_id)s
    """
    cursor.execute(query, {'p_user_id': user_id})
    sql_data = cursor.fetchall()
    filename = f'user_data\{(uuid.uuid4())}.csv'
    save_binary_to_file(sql_data, filename)
    return filename