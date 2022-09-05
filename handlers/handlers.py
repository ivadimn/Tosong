from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from config_data.resources import msgs
from config_data.config import AUDIO_DIR
from utils.youtube import get_audio, is_url_valid
from keyboards import kb_commands
from states.bot_states import BotState
from errors.errors import BadUrlError


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    locale = message.from_user.language_code.lower()
    msg = msgs[locale].WELCOME.format(message.from_user.full_name)
    await bot.send_message(message.chat.id, msg, reply_markup=kb_commands)


@dp.message_handler(commands=["help"])
async def chelp(message: types.Message):
    locale = message.from_user.language_code.lower()
    msg = "\n".join(["{0} - {1}".format(key, val) for key, val in msgs[locale].COMMANDS.items()])
    await bot.send_message(message.chat.id, msg)


@dp.message_handler(commands=["audio"])
async def audio(message: types.Message):
    locale = message.from_user.language_code.lower()
    msg = msgs[locale].AUDIO_MODE
    await BotState.url_audio.set()
    await bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=["text",], state=BotState.url_audio)
async def audio_url(message: types.Message, state: FSMContext):
    locale = message.from_user.language_code.lower()
    url = message.text
    uid = message.chat.id
    try:
        if not is_url_valid(url):
            raise BadUrlError(url)
        file = get_audio(url, AUDIO_DIR, uid)
        with open(file, "rb") as a:
            await bot.send_audio(message.chat.id, a)
    except BadUrlError as ex:
        await bot.send_message(message.chat.id, msgs[locale].BAD_URL.format(url))
    except Exception as ex:
        print(str(ex))
        await BotState.repeat.set()
        msg = "{0}\n{1}".format(msgs[locale].ERROR.format(str(ex)), msgs[locale].REPEAT)
        await bot.send_message(message.chat.id, msg)


@dp.message_handler(content_types=["text", ], state=BotState.repeat)
async def repeat(message: types.Message, state: FSMContext):
    locale = message.from_user.language_code.lower()
    answer = message.text
    if answer.lower() == "yes" or answer.lower() == "да":
        msg = msgs[locale].AUDIO_MODE
        await BotState.url_audio.set()
        await bot.send_message(message.chat.id, msg)
    else:
        await state.reset_data()
        await bot.send_message(message.chat.id, msgs[locale].SELECT_COMMAND, reply_markup=kb_commands)


