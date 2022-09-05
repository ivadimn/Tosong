from aiogram.dispatcher.filters.state import State, StatesGroup


class BotState(StatesGroup):
    url_audio = State()
    url_video = State()
    repeat = State()
