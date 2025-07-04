import discord

class ViewFecharCarrinho(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(BotaoFecharCarrinho())

class BotaoFecharCarrinho(discord.ui.Button):
    def __init__(self):
        super().__init__(label='❌ Fechar carrinho',style= discord.ButtonStyle.danger)
    async def callback(self, interaction: discord.Interaction):
        await interaction.channel.delete()

