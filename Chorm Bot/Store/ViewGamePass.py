import discord
from Store.ModalGamePass import ModalGamePass

class ViewGamePass(discord.ui.View):
    def __init__(self, nick_name):
        super().__init__(timeout=None)
        self.add_item(BotaoGamePass(nick_name))   

class BotaoGamePass(discord.ui.Button):
    def __init__(self, nick_name):
        super().__init__(label='Insira a 𝗚𝗮𝗺𝗲𝗣𝗮𝘀𝘀', style=discord.ButtonStyle.primary)
        self.nick_name = nick_name

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ModalGamePass(self.nick_name)) 