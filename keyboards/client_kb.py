from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

high_btn = KeyboardButton("/high")
audio_btn = KeyboardButton("/audio")
help_btn = KeyboardButton("/help")

kb_commands = ReplyKeyboardMarkup(resize_keyboard=True)
kb_commands.row(high_btn, audio_btn, help_btn)

