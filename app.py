import os
import sys
from typing import NoReturn

import discord
from dotenv import load_dotenv

from utils.activity import StatusManager
from utils.logger import Logger

class DiscordBot:
    def __init__(self):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
        self.logger = Logger()
        self.logger.rotate_log_file()
        
        load_dotenv()
        self._token = os.getenv('DISCORD_TOKEN')
        self._setup_client()
        
    def _setup_client(self) -> None:
        intents = discord.Intents.default()
        intents.dm_messages = True
        intents.messages = True
        self.client = discord.Client(intents=intents)
        self._register_events()
        
    def _register_events(self) -> None:
        @self.client.event
        async def on_ready() -> None:
            self.logger.info(f"Logged in as {self.client.user}")
            await self._initialize_status_manager()
            
        @self.client.event
        async def on_error(event, *args, **kwargs) -> None:
            self.logger.error(f"Error occurred in event {event}: {args}")
            
    async def _initialize_status_manager(self) -> None:
        try:
            status_manager = StatusManager(self.client, self.logger)
            self.client.loop.create_task(status_manager.update_status())
            self.logger.info("Status manager initialized successfully")
        except Exception as e:
            self.logger.error(f"Status manager initialization failed: {e}")
            
    def run(self) -> NoReturn:
        self.logger.info("Bot initialization started")
        try:
            self.client.run(self._token)
        except Exception as e:
            self.logger.error(f"Critical error during bot execution: {e}")
            sys.exit(1)

if __name__ == "__main__":
    bot = DiscordBot()
    bot.run()
