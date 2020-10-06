from discord.ext.commands import Context
from discord.ext.commands import Cog
from discord import Guild


class QueueGenerator:
    async def create_player(self, /):
        raise NotImplementedError

    async def send(self, ctx: Context, /):
        raise NotImplementedError


class QueueCog(Cog):
    def __init__(self, /):
        self.players = {}

    async def cleanup(self, guild: Guild, /):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass
