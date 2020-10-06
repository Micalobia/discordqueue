from discord import Guild
from discord import TextChannel
from discord.ext.commands import Context
from discord.ext.commands import Cog
from typing import Union


class QueueGenerator:
    async def create_player(self, /):
        raise NotImplementedError

    async def send(self, ctx: Union[Context, TextChannel], /):
        raise NotImplementedError

    def destroy(self, /):
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
            del self[guild]
        except KeyError:
            pass

    def __getitem__(self, index: Union[Guild, int], /):
        if isinstance(index, Guild):
            return self.players[index.id]
        elif isinstance(index, int):
            return self.players[index]
        else:
            raise TypeError('indicies must be guilds or guild ids')

    def __delitem__(self, index: Union[Guild, int], /):
        if isinstance(index, Guild):
            del self.players[index.id]
        elif isinstance(index, int):
            del self.players[index]
        else:
            raise TypeError('indicies must be guilds or guild ids')
