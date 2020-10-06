from discord import HTTPException
from discord.ext.commands import Context
import asyncio
from async_timeout import timeout
from .core import QueueGenerator
from typing import Iterable


class MusicPlayer:
    __slots__ = (
        'bot',
        'guild',
        'channel',
        'cog',
        'queue',
        'index',
        'next',
        'np',
        'leave_time',
        'poll_frequency',
        'current'
    )

    def __init__(self, ctx: Context, /, *, leave_time=300, poll_frequency=1):
        self.bot = ctx.bot
        self.guild = ctx.guild
        self.channel = ctx.channel
        self.cog = ctx.cog
        self.queue = []
        self.index = 0
        self.next = asyncio.Event()
        self.np = None
        self.leave_time = leave_time
        self.poll_frequency = poll_frequency
        self.current = None
        self.bot.loop.create_task(self.player_loop())

    def __len__(self, /):
        return len(self.queue)

    def __iter__(self, /):
        return len(self.queue)

    def __getitem__(self, index: int, /):
        return self.queue[index]

    def __setitem__(self, index: int, value: QueueGenerator, /):
        self.queue[index] = value

    def __delitem__(self, index: int, /):
        del self.queue[index]

    async def player_loop(self, /):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()
            if self.leave_time > 0:
                try:
                    async with timeout(self.leave_time):
                        while self.index >= len(self.queue):
                            await asyncio.sleep(self.poll_frequency)
                        generator = self.queue[self.index]
                except asyncio.TimeoutError:
                    return self.destroy()
            else:
                while self.index >= len(self.queue):
                    await asyncio.sleep(self.poll_frequency)
                generator = self.queue[self.index]
            source = await generator.create_player()
            self.current = source
            loop = self.bot.loop
            self.guild.voice_client.play(
                source,
                after=lambda _: loop.call_soon_threadsafe(self.next.set)
            )
            self.np = await generator.send(self.channel)
            await self.next.wait()
            source.cleanup()
            self.current = None
            self.index += 1
            try:
                await self.np.delete()
            except HTTPException:
                pass

    def destroy(self, /):
        for song in self.queue:
            song.destroy()
        return self.bot.loop.create_task(self.cog.cleanup(self.guild))

    def append(self, generator: QueueGenerator, /):
        self.queue.append(generator)

    def clear(self, /):
        self.queue.clear()

    def extend(self, other: Iterable[QueueGenerator], /):
        self.queue.extend(other)

    def insert(self, index: int, value: QueueGenerator):
        self.queue.insert(index, value)

    def pop(self, index=-1, /):
        self.queue.pop(index)

    def jump(self, index: int, /):
        if index < 0:
            index = 0
        if index > len(self):
            index = len(self)
        if index != self.index:
            self.index = index - 1
            self.guild.voice_client.stop()

    def skip(self, /):
        self.guild.voice_client.stop()

    def pause(self, /):
        self.guild.voice_client.pause()

    def resume(self, /):
        self.guild.voice_client.resume()

    def disconnect(self, /):
        return self.destroy()
