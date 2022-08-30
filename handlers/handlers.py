from aiogram import types
from loader import dp, bot
from config_data.resources import msgs


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    locale = message.from_user.language_code.lower()
    msg = msgs[locale].WELCOME.format(message.from_user.full_name)
    await bot.send_message(message.chat.id, msg)


@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    locale = message.from_user.language_code.lower()
    msg = "\n".join(["{0} - {1}".format(key, val) for key, val in msgs[locale].COMMANDS.items()])
    await bot.send_message(message.chat.id, msg)
