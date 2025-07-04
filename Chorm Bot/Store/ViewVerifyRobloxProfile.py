import discord
import asyncio
from Modules.embeds import embed_select
from Store.ViewOpcoesProdutos import ViewOpcoesProduto
from Store.ViewGamePass import ViewGamePass

class ViewVerifyRobloxProfile(discord.ui.View):
    def __init__(self, nome_produto_formatado, nickname_roblox, profile_url):
        super().__init__(timeout=None)
        self.add_item(SouEu(nome_produto_formatado, nickname_roblox))
        self.add_item(NãoSouEu(nome_produto_formatado, nickname_roblox))
        self.add_item(LinkPerfilButton(profile_url))

class SouEu(discord.ui.Button):
    def __init__(self, nome_produto, nickname_roblox):
        super().__init__(label='Sou eu', style=discord.ButtonStyle.green)
        self.nickname_roblox = nickname_roblox
        self.nome_produto = nome_produto


    async def callback(self, interaction: discord.Interaction):

        if self.nome_produto == 'robux':
            await interaction.message.delete()
            await interaction.response.send_message(view=ViewGamePass(self.nickname_roblox))
            return
        
        await interaction.response.send_message(embed=embed_select(self.nome_produto), view=ViewOpcoesProduto(self.nome_produto, nickname_roblox=self.nickname_roblox))
        await interaction.message.delete()


class NãoSouEu(discord.ui.Button):
    def __init__(self, nome_produto, nickname_roblox):
        super().__init__(label='Não sou eu', style=discord.ButtonStyle.danger)
        self.nickname_roblox = nickname_roblox
        self.nome_produto = nome_produto

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(thinking=True)
        await interaction.message.delete()

        from Store.ViewInsiraNickname import ViewInsiraNickname
        embed2 = discord.Embed(title='Digite seu NickName do Roblox')
        embed2.color = discord.Color.from_rgb(255,0,0)
        await interaction.followup.send(embed=embed2, view=ViewInsiraNickname(self.nome_produto)) 



class LinkPerfilButton(discord.ui.Button):
    def __init__(self, profile_url):
        super().__init__(label='Ver Perfil no Roblox', style=discord.ButtonStyle.link, url=profile_url)
