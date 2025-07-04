#IMPORTAÇÕES
import config
import discord
from Modules.dbfunctions import get_dados_produto
from Modules.embeds import embed_select
from Store.ViewFecharCarrinho import ViewFecharCarrinho
from Store.ViewInsiraNickname import ViewInsiraNickname
from Store.ViewOpcoesProdutos import ViewOpcoesProduto

# BOTÃO ABRIR CARRINHO (Responsável por abrir um ticket)

# VIEW PASSA AS VARIÁVEIS PARA TODo RESTO
class ViewAbrirCarrinho(discord.ui.View):
    def __init__(self, nome_produto_formatado):
        super().__init__(timeout=None)
        self.add_item(BotaoAbrirCarrinho(nome_produto_formatado))



class BotaoAbrirCarrinho(discord.ui.Button):
    def __init__(self, nome_produto):
        super().__init__(label='🛒 Abrir Carrinho',style=discord.ButtonStyle.green)
        self.nome_produto = nome_produto

    async def callback(self, interaction: discord.Interaction):

        # ----- CRIAÇÃO DO TICKET -----
        categoria_tickets = interaction.guild.get_channel(config.CATEGORIA_TICKETS_ID)
        dados_produto = get_dados_produto(self.nome_produto)

        ticket_channel_name = f'{dados_produto['emoji']} Comprar {self.nome_produto.capitalize()}-{interaction.user.name}-{interaction.user.id}'
        
        ticket_channel = await interaction.guild.create_text_channel(ticket_channel_name, category=categoria_tickets, overwrites={
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
            })
    
        # ----- RESPOSTA A INTERAÇÃO -----
        embed = discord.Embed(title=f'{self.nome_produto.upper()} ! | Chorm Store.', description=f'''・ Seu carrinho foi aberto com sucesso em {ticket_channel.mention}''',)
        embed.color = discord.Color.from_rgb(142, 38, 44)
        embed.set_thumbnail(url=config.URL_LOGO)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        # ----- ENVIA FECHAR CARRINHO NO TICKET -----
        embed_fechar_carrinho = discord.Embed(title=f'Este é seu carrinho {interaction.user}!', description='Para fazer a compra siga as instruções do bot abaixo:')
        embed_fechar_carrinho.color = discord.Color.from_rgb(255,0,0)

        await ticket_channel.send(embed=embed_fechar_carrinho, view=ViewFecharCarrinho())

        # ----- ENVIA FORMS DE BUSCA ROBLOX -----
        if dados_produto['busca_user_roblox']:
            embed_digite_usuario = discord.Embed(title='Digite seu NickName do Roblox')
            embed_digite_usuario.color = discord.Color.from_rgb(255,0,0)

            view = ViewInsiraNickname(self.nome_produto)
            await ticket_channel.send(embed=embed_digite_usuario, view=view)

        else:
            await ticket_channel.send(embed=embed_select(self.nome_produto), view=ViewOpcoesProduto(self.nome_produto))

