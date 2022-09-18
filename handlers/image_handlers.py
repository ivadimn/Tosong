import os
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from config_data.resources import msgs
from keyboards import kb_commands, kb_yes_no
from states.bot_states import BotState


@dp.message_handler(commands=["image"], state="*")
async def audio(message: types.Message, state: FSMContext):
    locale = message.from_user.language_code.lower()
    msg = msgs[locale].IMAGE_STUB
    await bot.send_message(message.chat.id, msg)