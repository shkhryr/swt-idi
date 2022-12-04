from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from utils.messages import EVENTS, ADD_EVENT, PLACES, CAFE, REGISTER_BUTTON, MALE, FEMALE, RETURN, LOCATION_BUTTON, \
    LIKE, DISLIKE

start_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
start_button_1 = KeyboardButton(PLACES)
start_button_2 = KeyboardButton(CAFE)
start_button_3 = KeyboardButton(EVENTS)
start_button_4 = KeyboardButton(ADD_EVENT)
start_markup.add(*[start_button_1, start_button_2, start_button_3, start_button_4])

register_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
register_button_1 = KeyboardButton(REGISTER_BUTTON)
register_markup.add(*[register_button_1])

gender_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
gender_button_1 = KeyboardButton(MALE)
gender_button_2 = KeyboardButton(FEMALE)
gender_markup.add(*[gender_button_1, gender_button_2])

return_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
return_button_1 = KeyboardButton(LIKE)
return_button_2 = KeyboardButton(DISLIKE)
return_button_3 = KeyboardButton(RETURN)
return_markup.add(*[return_button_1, return_button_2, return_button_3])

location_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
location_button_1 = KeyboardButton(LOCATION_BUTTON, request_location=True)
location_markup.add(*[location_button_1])


