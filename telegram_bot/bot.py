from config import API_TOKEN
from get_data import get_info
import logging
from aiogram import Bot, Dispatcher, executor, types
from qr_code_recognition import read_qr_code_from_bytes
from io import BytesIO
import numpy as np
import requests
from bs4 import BeautifulSoup
from data_service import add_user, add_check
import random
import datetime

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



    
@dp.message_handler(commands=['info', 'help', 'start'])
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
        check_place, check_items, check_sum, check_fd, check_fn, check_fpd, check_date = get_info(qr_code_text)
        add_check(check_fn, check_fd, check_fpd, tg_user_id, '1ofd', check_place, check_sum, check_date)
        goods = ''
        for item in check_items:
            goods += (f"{item['name']} {item['price'] / 100} ✕ {item['quantity']}    {item['sum'] / 100}\n")
        await message.answer(f'{goods}')




if __name__ == '__main__':
    executor.start_polling(dp)
