from config import API_TOKEN
from get_data import get_info
import logging
from aiogram import Bot, Dispatcher, executor, types
from qr_code_recognition import read_qr_code_from_bytes
from io import BytesIO
import numpy as np
import requests
from bs4 import BeautifulSoup
from data_service import add_user
import random

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



    
@dp.message_handler(commands=['info', 'help', 'start'])
async def give_info(message: types.Message):
    await message.reply(
        f"Hi {message.from_user.first_name},\nthis bot takes qr-code and adds info about your purchase into database")

@dp.message_handler(commands=['take_photo'])
async def take_photo(message: types.Message):
    @dp.message_handler(content_types=['photo'])
    async def respond_photo(message: types.Message):
        #add_user(message.chat['id'], message.date)
        qr_code_bytes = BytesIO()
        await message.photo[-1].download(destination_file = qr_code_bytes)
        qr_code_bytes = qr_code_bytes.getvalue()
        qr_code_bytes = np.frombuffer(qr_code_bytes, dtype=np.int8)
        qr_code_text = read_qr_code_from_bytes(qr_code_bytes)
        if qr_code_text == '':
            qr_code_text = 'Can not extract qr-code'
            await message.reply(qr_code_text)
        else:
            user_id, retail_place_address, items = get_info(qr_code_text)
            goods = ''
            for item in items:
                goods += (f"{item['name']} {item['price'] / 100} ✕ {item['quantity']}    {item['sum'] / 100}\n")
            await message.reply(goods)

if __name__ == '__main__':
    executor.start_polling(dp)
