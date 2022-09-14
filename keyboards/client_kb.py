from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

high_btn = KeyboardButton("/high")
audio_btn = KeyboardButton("/audio")
help_btn = KeyboardButton("/help")

kb_commands = ReplyKeyboardMarkup(resize_keyboard=True)
kb_commands.row(high_btn, audio_btn, help_btn)

yes_btn_en = KeyboardButton("Yes")
no_btn_en = KeyboardButton("No")
kb_yes_no_en = ReplyKeyboardMarkup(resize_keyboard=True)
kb_yes_no_en.row(yes_btn_en, no_btn_en)

yes_btn_ru = KeyboardButton("Да")
no_btn_ru = KeyboardButton("Нет")
kb_yes_no_ru = ReplyKeyboardMarkup(resize_keyboard=True)
kb_yes_no_ru.row(yes_btn_ru, no_btn_ru)

kb_yes_no = {"ru": kb_yes_no_ru, "en": kb_yes_no_en}
