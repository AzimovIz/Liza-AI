import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from core import Core

router = Router()

bot: Bot
dp: Dispatcher

nl = "\n"

core = Core()

logger = logging.getLogger("root")


@router.message(F.text == "/start")
async def command_handler(msg: types.Message, *args, **kwargs):
    if msg.from_user.id not in kwargs["bot"].allow_ids:
        await msg.reply(
            text="Только хозяин может меня использовать!"
        )
        return

    await msg.reply("Я тут)")


@router.message(F.text)
async def msg_handler(msg: types.Message, *args, **kwargs):
    if msg.from_user.id not in kwargs["bot"].allow_ids:
        await msg.reply(
            text="Только хозяин может меня использовать!"
        )
        return

    # TODO: тут нада отправка в ядро
    await msg.reply("Это конечно все здорово, но пока я туплю)")


@router.message(F.voice)
async def voice_handler(msg: types.Message, *args, **kwargs):
    if msg.from_user.id not in kwargs["bot"].allow_ids:
        await msg.reply(
            text="Только хозяин может меня использовать!"
        )
        return
    file_id = msg.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "last_bot_voice.wav")
    text = core.recognize_file("last_bot_voice.wav")
    await msg.reply(f"Услышала:\n{text}")
    # TODO: тут нада отправка в ядро
    await msg.reply("но пока я туплю)")


async def run_client(bot_token, allow_isd):
    global bot, dp
    try:
        bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
        bot.allow_ids = allow_isd
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(router)

    except:
        return

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


async def stop_client():
    global dp
    try:
        await dp.stop_polling()
    except:
        pass


async def start(core: Core):
    manifest = {
        "name": "Плагин телеграм бота",
        "version": "1.0",

        "default_options": {
            "bot_token": "12345:qwerty",
            "allow_isd": [12345, 12345]
        },
    }
    return manifest


async def start_with_options(core: Core, manifest: dict):
    bot_token = manifest["options"]["bot_token"]
    allow_isd = manifest["options"]["allow_isd"]
    asyncio.run_coroutine_threadsafe(run_client(bot_token, allow_isd), asyncio.get_running_loop())