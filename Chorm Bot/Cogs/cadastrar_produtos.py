import discord
from discord.ext import commands
from discord import app_commands
from Modules.database import produtos_collection
from Store import ModalCadastrarProdutos 
from Modules.generalfunctions import url_imagem_valida

class CadastroProduto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.tree.add_command(self.cadastrar_produto)

    @app_commands.command(name="cadastrar_produto", description="Cadastra um novo produto no banco de dados.")
    @app_commands.choices(
        busca_user_roblox=[
            app_commands.Choice(name='sim', value='True'),
            app_commands.Choice(name='não', value=''),
        ],
        quantidade_produtos=[
            app_commands.Choice(name='1 produto', value=1),
            app_commands.Choice(name='2 produtos', value=2),
            app_commands.Choice(name='3 produtos', value=3),
            app_commands.Choice(name='4 produtos', value=4),
            app_commands.Choice(name='5 produtos', value=5),
            app_commands.Choice(name='+ de 5 produtos', value=10),
        ],
        pronome_produto=[
            app_commands.Choice(name='Masculino', value='o'),
            app_commands.Choice(name='Feminino', value='a'),
        ]
    )
    async def cadastrar_produto(
        self,
        interaction: discord.Interaction,
        nome_produto: str,
        categoria: discord.CategoryChannel,
        nome_canal: str,
        emoji: str,
        busca_user_roblox: app_commands.Choice[str],
        url_vitrine: str,
        quantidade_produtos: app_commands.Choice[int],
        pronome_produto: app_commands.Choice[str],
        cor_hex_opcional: str = None
    ):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)
            return

        if produtos_collection.find_one({'nome_produto': nome_produto.lower().strip()}):
            await interaction.response.send_message( f"O produto {nome_produto} já existe no Banco de Dados. Para modificá-lo, utilize a estrutura já existente", ephemeral=True)
            return
        
        if not url_imagem_valida(url_vitrine):
            await interaction.response.send_message(f"A URL `{url_vitrine}` é inválida.", ephemeral=True)
            return

        modal = ModalCadastrarProdutos(
            nome_produto,
            categoria,
            nome_canal,
            emoji,
            bool(busca_user_roblox.value),
            url_vitrine,
            quantidade_produtos.value,
            pronome_produto.value,
            cor_hex_opcional
        )
        await interaction.response.send_modal(modal)

async def setup(bot: commands.Bot):
    await bot.add_cog(CadastroProduto(bot))
