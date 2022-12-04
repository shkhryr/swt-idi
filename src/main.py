import asyncio
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils import db
from utils.db import register_user
from utils.locations import location_randomizer
from utils.buttons import start_markup, register_markup, gender_markup, return_markup
from utils.messages import (
    ADD_EVENT, EVENTS, PLACES, CAFE, WELCOME_TEXT, REGISTER, GENDER, AGE, REGISTER_BUTTON,
    AGE_AGAIN, REGISTER_SUCCESS, REGISTERED_ALREADY, GENDER_AGAIN, RETURN, MAIN_MENU, LIKE, DISLIKE
)

load_dotenv()

loop = asyncio.get_event_loop()
storage = MemoryStorage()
bot = Bot(getenv("BOT_TOKEN"), parse_mode="HTML")
dp = Dispatcher(bot, storage=storage, loop=loop)

BASE_DIR: Path = Path(__file__).resolve().parent.parent
ADMINS_ID: list = list(map(int, getenv("ADMINS_ID").split()))


class UserRegistration(StatesGroup):
    gender = State()
    age = State()
    finish = State()


# Answer to all bot commands
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    # await bot.send_location(message.chat.id, latitude=41.31171299655966, longitude=69.27955993180066)
    # return await bot.send_message(message.chat.id, LOCATION, reply_markup=location_markup)
    if db.user_exists(message.chat.id):
        await bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=start_markup)
    else:
        await bot.send_message(message.chat.id, REGISTER, reply_markup=register_markup)


@dp.message_handler(text=REGISTER_BUTTON)
async def register_start(message: Message):
    if not db.user_exists(message.chat.id):
        await bot.send_message(message.chat.id, GENDER, reply_markup=gender_markup)
        await UserRegistration.gender.set()
    else:
        await bot.send_message(message.chat.id, REGISTERED_ALREADY, reply_markup=start_markup)


@dp.message_handler(state=UserRegistration.gender)
async def get_gender(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == '👨 Male':
            data["gender"] = "M"
        elif message.text == '👩 Female':
            data["gender"] = "F"
        else:
            await bot.send_message(message.chat.id, GENDER_AGAIN, reply_markup=gender_markup)
            return await UserRegistration.gender.set()

    await bot.send_message(message.chat.id, AGE, reply_markup=ReplyKeyboardRemove())
    await UserRegistration.age.set()


@dp.message_handler(state=UserRegistration.age)
async def finish(message: Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            age = int(message.text)
            if age > 0:
                data["age"] = message.text
                await register_user(message.chat.id, age=data['age'], gender=data['gender'])
                await state.finish()
                return await bot.send_message(message.chat.id, REGISTER_SUCCESS, reply_markup=start_markup)
        except ValueError:
            pass
        await bot.send_message(message.chat.id, AGE_AGAIN)
        return await UserRegistration.age.set()


@dp.message_handler(text=CAFE)
async def cafe_command(message: Message):
    if db.user_exists(message.chat.id):
        text_message, maps_message, longitude, latitude = location_randomizer(location_type=CAFE)

        await bot.send_message(message.chat.id, text_message)
        await bot.send_location(message.chat.id, latitude=latitude, longitude=longitude)
        return await bot.send_message(message.chat.id, maps_message, disable_web_page_preview=True, reply_markup=return_markup)

    else:
        return await bot.send_message(message.chat.id, REGISTER, reply_markup=register_markup)


@dp.message_handler(text=PLACES)
async def places_command(message: Message):
    if db.user_exists(message.chat.id):
        text_message, maps_message, longitude, latitude = location_randomizer(location_type=PLACES)

        await bot.send_message(message.chat.id, text_message)
        await bot.send_location(message.chat.id, latitude=latitude, longitude=longitude)
        return await bot.send_message(message.chat.id, maps_message, disable_web_page_preview=True, reply_markup=return_markup)
    else:
        return await bot.send_message(message.chat.id, REGISTER, reply_markup=register_markup)


@dp.message_handler(text=EVENTS)
async def events_command(message: Message):
    if db.user_exists(message.chat.id):
        text_message, maps_message, longitude, latitude = location_randomizer(location_type=EVENTS)

        await bot.send_message(message.chat.id, text_message)
        await bot.send_location(message.chat.id, latitude=latitude, longitude=longitude)
        return await bot.send_message(message.chat.id, maps_message, disable_web_page_preview=True, reply_markup=return_markup)
    else:
        return await bot.send_message(message.chat.id, REGISTER, reply_markup=register_markup)


@dp.message_handler(text=ADD_EVENT)
async def add_event_command(message: Message):
    if db.user_exists(message.chat.id):
        await bot.send_message(message.chat.id, "Under Development 🚧")
    else:
        return await bot.send_message(message.chat.id, REGISTER, reply_markup=register_markup)


@dp.message_handler(text=[RETURN, LIKE, DISLIKE])
async def return_command(message: Message):
    if db.user_exists(message.chat.id):
        message_to_send = MAIN_MENU
    else:
        return await bot.send_message(message.chat.id, REGISTER, reply_markup=register_markup)

    await bot.send_message(message.chat.id, message_to_send, reply_markup=start_markup)

