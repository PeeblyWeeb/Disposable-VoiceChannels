from discord.ext import commands

import breadcord


class UserVoiceChannels(breadcord.module.ModuleCog):
    def __init__(self, module_id: str):
        super().__init__(module_id)
        self.active_channels = []

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        for channel in self.active_channels:
            if len(channel.voice_states) == 0:
                self.active_channels.remove(channel)
                await channel.delete()
        if (
                after.channel is None
                or before.channel == after.channel
                or after.channel.id != self.settings.creation_channel_id.value
        ):
            return
        channel = await member.guild.create_voice_channel(
            f"{member.name}'s Channel",
            category=member.guild.get_channel(self.settings.creation_category_id.value),
            reason="User created voice channel!"
        )
        await member.move_to(channel)
        await channel.set_permissions(member, manage_channels=True, move_members=True, priority_speaker=True)
        self.active_channels.append(channel)


async def setup(self):
    await self.add_cog(UserVoiceChannels('uservoicechannels'))
