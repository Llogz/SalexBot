from dataclasses import dataclass
from typing import List
import discord
import asyncio
import time

@dataclass
class StatusConfig:
    UPDATE_INTERVAL: int = 10
    STATUSES: List[str] = (
        "v0.0.2 || /shelp",
        "Vodka or beer? || /shelp",
        "Listening on {server_count} servers",
        "Powered by caffeine",
        "Bot in action || /shelp",
        "On a mission...",
        "Your server’s best friend",
        "Code, coffee & chaos",
        "Hunting bad servers",
        "Bots don’t sleep",
        "Fixing issues... slowly",
        "Chatting with {server_count} servers",
        "Packets over feelings",
        "Need help? Try /shelp",
        "Uptime: {uptime}",
        "In a galaxy far...",
        "Caffeine, code & creativity",
        "Server admin’s best friend",
        "One command away from fixing it",
        "Coding with passion... and coffee",
        "I’m on a bug hunt",
        "Making servers better",
        "Unfortunately, I'm just a bot((",
    )

class StatusManager:
    def __init__(self, client: discord.Client, logger):
        self.client = client
        self.logger = logger
        self.status_index = 0
        self.start_time = time.time()
        self.config = StatusConfig()

    def _get_uptime(self) -> str:
        uptime_seconds = time.time() - self.start_time
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        return f"{hours}h {minutes}m {seconds}s"

    def _get_next_status(self, server_count: int) -> discord.CustomActivity:
        status_text = self.config.STATUSES[self.status_index].format(
            server_count=server_count,
            uptime=self._get_uptime()
        )
        self.status_index = (self.status_index + 1) % len(self.config.STATUSES)
        return discord.CustomActivity(name=status_text)

    async def update_status(self) -> None:
        while True:
            try:
                server_count = len(self.client.guilds)
                new_status = self._get_next_status(server_count)
                await self.client.change_presence(
                    status=discord.Status.idle,
                    activity=new_status
                )
                self.logger.status(f'Status updated: "{new_status.name}"')
            except Exception as e:
                self.logger.error(f"Status update failed: {e}")
            await asyncio.sleep(self.config.UPDATE_INTERVAL)
