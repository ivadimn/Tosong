from aiogram import executor
from loader import dp, bot
from aiogram.types import BotCommand
from config_data.config import COMMANDS
import handlers

url = "https://www.youtube.com/watch?v=9BMwcO6_hyA"
VIDEO_DIR = "videos"
AUDIO_DIR = "audios"


async def on_startup(_):
    await bot.set_my_commands(
        [BotCommand(*command) for command in COMMANDS]
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


