# ===== IMPORTS =====
import config
import discord
import random
# ===== DATABASE =====
from Modules.database import produtos_collection
# ===== MODULES =====
from Modules.generalfunctions import formatar_produto
from Modules.dbfunctions import gerar_embed_vitrine, status_loja
# ===== VIEWS =====
from Store.ViewAbrirCarrinho import ViewAbrirCarrinho

##--- Importações
usuarios_produtos = {}
class ModalCadastrarProdutos(discord.ui.Modal):
    def __init__(self, bot, nome_produto, categoria, nome_canal, emoji, busca_user_roblox, url_vitrine, qty_produtos, pronome_produto, cor_hex_opcional):
        
        self.bot = bot
        self.nome_produto = nome_produto
        self.categoria = categoria
        self.categoria_id = categoria.id
        self.nome_canal = nome_canal
        self.emoji = emoji
        self.busca_user_roblox = busca_user_roblox
        self.url_vitrine = url_vitrine
        self.pronome_produto = pronome_produto
        self.cor_hex_opcional = cor_hex_opcional

        # + de 5 produtos
        if qty_produtos > 5:
            super().__init__(title='Produto1 | Preço1 / Produto2 | Preço2')

            campo = discord.ui.TextInput(label=f'Produtos', placeholder='X-Burguer | 10.99 / Cachorro Quente | 7.99 / Pastel de Carne | 5,50 / Batata Frita | 6,99', style=discord.TextStyle.long)
            self.add_item(campo)

        # 5 produtos para baixo
        else:
            super().__init__(title='Use a estrutura: Nome | Preço')

            for i in range(qty_produtos):
                campo = discord.ui.TextInput(label=f'Produto {i + 1}', placeholder=random.choice(config.EXEMPLOS_PRODUTOS), style=discord.TextStyle.short)
                self.add_item(campo)
        

    async def on_submit(self, interact: discord.Interaction):
        produtos_dict = {}

        # + de 5 produtos
        if len(self.children) == 1 and self.children[0].style == discord.TextStyle.long:
            texto = self.children[0].value
            pares = texto.split('/')
            for par in pares:
                try:
                    nome, preco = par.strip().split('|')
                    produtos_dict[nome.strip()] = float(preco.strip().replace(',', '.'))
                except:
                    await interact.response.send_message("Formato inválido em: " + par, ephemeral=True)
                    return
            
            if len(produtos_dict) > 25 or len(produtos_dict) < 1:
                await interact.response.send_message(f"O campo deve possuir entre 1 a 25 produtos, o Discord não permite nem mais nem menos que isso. Reenvie o comando.", ephemeral=True)
                return 

        # 5 produtos para baixo
        else:
            for campo in self.children:
                try:
                    nome, preco = campo.value.strip().split('|')
                    produtos_dict[nome.strip()] = float(preco.strip().replace(',', '.'))
                except:
                    await interact.response.send_message(f"Formato inválido em: `{campo.value}`", ephemeral=True)
                    return


        # Cria o canal do produto
        canal = await interact.guild.create_text_channel(self.nome_canal, category=self.categoria)

        # Formata produto
        produto_formateddb = formatar_produto(self.nome_produto)
        # Cria o dicionário com os dados recebidos da __init__
        dados_produto = {
            "nome_produto": produto_formateddb,
            "id_canal": canal.id,
            "emoji": self.emoji,
            "busca_user_roblox": self.busca_user_roblox,
            "url_vitrine": self.url_vitrine,
            "pronome_produto": self.pronome_produto,
            "cor": self.cor_hex_opcional,
            "produtos": produtos_dict
        }
        produtos_collection.insert_one(dados_produto)

        embed= gerar_embed_vitrine(produto_formateddb, self.bot)
        view = ViewAbrirCarrinho(produto_formateddb if status_loja() == 'on' else None)

        await canal.send(embed=embed, view=view)
        
        await interact.response.send_message("Produto(s) cadastrado(s) com sucesso!", ephemeral=True)




        