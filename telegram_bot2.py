# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 13:14:10 2024

@author: User
"""

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from prettytable import PrettyTable
import aiohttp
import logging
from ttoken import token
 

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Здравствуйте! Используйте команды /Зарплата_по_квалификациям, /Зарплата_по_стажам, "
                        "/Ящик_с_усами  для получения данных.")


async def format_and_send_table(data, message):
    """Функция для форматирования таблицы и отправки"""
    table = PrettyTable()
    table.field_names = list(data[0].keys())
    for row in data:
        table.add_row(row.values())
    await message.answer(f"<pre>{table}</pre>", parse_mode='HTML')

async def process_response(response, message):
    """Функция для обработки ответа от сервера"""
    if response.status_code == 200:
        try:
            data = response.json()
            await format_and_send_table(data, message)
        except ValueError:
            # Если не удалось декодировать JSON, отправьте текстовое сообщение
            await message.answer("Ошибка: не удалось получить данные в формате JSON.")
    else:
        # Отправка текстового ответа с описанием ошибки
        await message.answer(
            f"Не удалось получить данные с сервера. Код ошибки: {response.status_code}.\nОтвет сервера: {response.text}")


@dp.message_handler(commands=['Зарплата_по_квалификациям'])
async def send_data(message: types.Message):
    response = requests.get("http://127.0.0.1:5001/Salgrade")
    await process_response(response, message)



@dp.message_handler(commands=['Зарплата_по_стажам'])
async def send_data(message: types.Message):
    response = requests.get("http://127.0.0.1:5001/Salexp")
    await process_response(response, message)



@dp.message_handler(commands=['Ящик_с_усами'])
async def send_histogram(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:5001/box") as response:
            if response.status == 200:
                img_data = await response.read()
                await message.answer_photo(photo=img_data, caption="Распределение максимальных зарплат!")
            else:
                await message.answer(f"Не удалось получить гистограмму с сервера. Код ошибки: {response.status}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
