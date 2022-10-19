import os
from pyrogram import Client
from bot import Config, LOGGER
from bot.helpers.kkbox.kkbox_helper import kkbox
from bot.helpers.utils.auth_check import get_chats
from bot.helpers.tidal_func.events import checkAPITidal
from bot.helpers.tidal_func.settings import TIDAL_SETTINGS, TIDAL_TOKEN

plugins = dict(
    root="bot/modules"
)

async def loadConfigs():
    LOGGER.info('Loading Tidal DL Configs....')
    TIDAL_SETTINGS.read()
    TIDAL_TOKEN.read("./tidal-dl.token.json")
    await checkAPITidal()
    # KKBOX
    if not "" in {Config.KKBOX_EMAIL, Config.KKBOX_KEY, Config.KKBOX_PASSWORD}:
        LOGGER.info("Loading KKBOX Configs....")
        await kkbox.login()

class Bot(Client):
    def __init__(self):
        super().__init__(
            "AIO-Music-Bot",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.TG_BOT_TOKEN,
            plugins=plugins,
            workdir=Config.WORK_DIR
        )

    async def start(self):
        await super().start()

        await loadConfigs()
        
        if Config.ANIT_SPAM_MODE == "True":
            LOGGER.info("ANTI-SPAM MODE ON")
        await get_chats()
        LOGGER.info("❤ MUSIC HELPER BOT BETA v0.1 STARTED SUCCESSFULLY ❤")

    async def stop(self, *args):
        await super().stop()
        LOGGER.info('Bot Exited Successfully ! Bye..........')

if __name__ == "__main__":
    if not os.path.isdir(Config.DOWNLOAD_BASE_DIR):
        os.makedirs(Config.DOWNLOAD_BASE_DIR)
    app = Bot()
    app.run()
