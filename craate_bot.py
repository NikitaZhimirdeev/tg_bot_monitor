from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import settings
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot, storage=storage)