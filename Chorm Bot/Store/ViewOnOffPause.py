import config
import discord
from Modules.dbfunctions import status_loja, ligar_loja, desligar_loja, pausar_loja, embed_status, reset_produtos


"""ON OF PAUSE"""

class ViewBotoesOnOffPause(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(BotaoOn())
        self.add_item(BotaoOff())
        self.add_item(BotaoPause())


class BotaoOn(discord.ui.Button): 
    def __init__(self):
        super().__init__(label='On', style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        if status_loja() == 'on':
            await interaction.followup.send("A loja já está aberta.", ephemeral=True)
            return

        ligar_loja()
        
        status_canal = interaction.guild.get_channel(config.STATUS_CHANNEL_ID)
        await status_canal.purge(limit=3)
        await status_canal.send(embed=embed_status(interaction))

        await reset_produtos(interaction.client)

        await interaction.followup.send("Loja On!", ephemeral=True)


class BotaoOff(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Off', style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if status_loja() == 'off':
            await interaction.followup.send("A loja já está fechada.", ephemeral=True)
            return

        desligar_loja()

        status_canal = interaction.guild.get_channel(config.STATUS_CHANNEL_ID)
        await status_canal.purge(limit=3)
        await status_canal.send(embed=embed_status(interaction))

        await reset_produtos(interaction.client)

        await interaction.followup.send("Loja Off!", ephemeral=True)


class BotaoPause(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Pausar Loja', style=discord.ButtonStyle.grey)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if status_loja() == 'pause':
            await interaction.followup.send("A loja já está pausada.", ephemeral=True)
            return

        pausar_loja()

        status_canal = interaction.guild.get_channel(config.STATUS_CHANNEL_ID)
        await status_canal.purge(limit=3)
        await status_canal.send(embed=embed_status(interaction))

        await reset_produtos(interaction.client)

        await interaction.followup.send("Loja pausada!", ephemeral=True)
