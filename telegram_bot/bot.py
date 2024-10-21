from config import API_TOKEN
from get_data import get_info
import logging
from aiogram import Bot, Dispatcher, executor, types
from qr_code_recognition import read_qr_code_from_bytes
from io import BytesIO
import numpy as np
import requests
from bs4 import BeautifulSoup
from add_data import add_user, add_receipt, add_items, delete_user, find_receipt
from give_data import give_all_data
import uuid

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['info'])
async def give_info(message: types.Message):
    await message.answer(f"Hi {message.from_user.first_name},\nthis bot takes qr-code and adds info about your purchase into database")


@dp.message_handler(content_types=['photo'])
async def respond_photo(message: types.Message):
    tg_user_id = str(message.chat.id)
    create_date = message.date
    add_user(tg_user_id, create_date)
    qr_code_bytes = BytesIO()
    await message.photo[-1].download(destination_file = qr_code_bytes)
    qr_code_bytes = qr_code_bytes.getvalue()
    qr_code_bytes = np.frombuffer(qr_code_bytes, dtype=np.int8)
    qr_code_text = read_qr_code_from_bytes(qr_code_bytes)
    if qr_code_text == '':
        qr_code_text = 'Can not extract qr-code'
        await message.answer(qr_code_text)
    else:
        receipt_place, receipt_items, receipt_sum, receipt_fd, receipt_fn, receipt_fpd, receipt_date = get_info(qr_code_text)
        receipt_id = str(uuid.uuid4())
        if not find_receipt(receipt_fn, receipt_fd, receipt_fpd):
            add_receipt(receipt_fn, receipt_fd, receipt_fpd, tg_user_id, '1ofd', receipt_place, receipt_sum, receipt_date, receipt_id)
            goods = ''
            for item in receipt_items:
                goods += (f"{item['name']} {item['price'] / 100} ✕ {item['quantity']}    {item['sum'] / 100}\n")
                add_items(item['name'], item['price'] / 100, item['quantity'], item['sum'] / 100, receipt_id)
            await message.answer(f'{goods}')
        else:
            await message.answer(f'dublicate receipt')


@dp.message_handler(commands=['delete_my_data'])
async def delete_data(message: types.Message):
    tg_user_id = str(message.chat.id)
    delete_user(tg_user_id)
    await message.answer('your data was deleted successfully')

@dp.message_handler(commands=['give_all_purches'])
async def give_purches(message: types.Message):
    tg_user_id = str(message.chat.id)
    filename = give_all_data(tg_user_id)
    await message.reply_document(open(filename, 'rb'))



if __name__ == '__main__':
    executor.start_polling(dp)
