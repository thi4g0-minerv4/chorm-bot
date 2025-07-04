#IMPORTAÇÕES
import discord
from Modules.roblox import *

from Store.ModalInsiraNickname import ModalInsiraNickname


class ViewInsiraNickname(discord.ui.View):
    def __init__(self, nome_produto_formatado):
        super().__init__(timeout=None)
        self.add_item(BotaoInsiraNickname(nome_produto_formatado))

class BotaoInsiraNickname(discord.ui.Button):
    def __init__(self, nome_produto_formatado):
        super().__init__(label="Insira seu 𝗡𝗶𝗰𝗸𝗡𝗮𝗺𝗲", style=discord.ButtonStyle.primary)
        self.nome_produto = nome_produto_formatado

    async def callback(self, interaction: discord.Interaction):
        modal = ModalInsiraNickname(self.nome_produto)
        await interaction.response.send_modal(modal)




