# ===== IMPORTS =====
import discord
import config
from Store.ViewFormasPagamento import ViewFormasPagamento
from Modules.database import produtos_collection
from Modules.generalfunctions import formatar_produto


# ============ VIEW PRINCIPAL ============

class ViewOpcoesProduto(discord.ui.View):
    def __init__(self, nome_produto_formatado, nickname_roblox=None):
        super().__init__(timeout=None)
        self.add_item(MenuSelecaoProdutos(nome_produto_formatado, nickname_roblox))


# ============ SELECT ============

class MenuSelecaoProdutos(discord.ui.Select):
    def __init__(self, nome_produto, nickname_roblox):
        self.nickname_roblox = nickname_roblox
        self.produtos = self.buscar_produtos(nome_produto)

        opcoes = []

        for nome_item, preco in self.produtos.items():
            preco_str = f'R${preco:.2f}'.replace('.', ',')
            label = nome_item.upper()
            value = f"{nome_item}|{preco}"
            opcoes.append(
                discord.SelectOption(
                    emoji=config.MAIN_EMOJI,
                    label=label,
                    value=value,
                    description=f'Preço: {preco_str}'
                )
            )

        super().__init__(placeholder="Selecione a opção desejada:", min_values=1, max_values=1, options=opcoes)

    def buscar_produtos(self, nome_produto):
        nome_formatado = formatar_produto(nome_produto)
        dados = produtos_collection.find_one({"nome_produto": nome_formatado})
        return dados.get("produtos", {}) if dados else {}

    async def callback(self, interaction: discord.Interaction):
        nome_produto, preco = self.values[0].split('|')
        preco = float(preco)

        embed = discord.Embed(
            title=f'{config.MAIN_EMOJI} Pedido de {interaction.user.name}',
            description="Está quase lá, para **avançarmos** com a venda, selecione o **método de pagamento abaixo.**"
        )

        if self.nickname_roblox:
            embed.add_field(
                name=f'{config.ROBLOX_EMOJI} Roblox Nick:',
                value=self.nickname_roblox,
                inline=True
            )

        embed.add_field(
            name=f'{config.MONEY_EMOJI} Valor Final:',
            value=f"R$ {preco:.2f}".replace('.', ','),
            inline=True
        )

        embed.add_field(
            name=f'{config.MONEY_EMOJI} Produto selecionado:',
            value=nome_produto,
            inline=True
        )

        embed.color = discord.Color.from_rgb(255, 0, 0)

        await interaction.message.delete()
        await interaction.response.send_message(embed=embed)

        embed_pagamento = discord.Embed(
            title='Após a compra envie o comprovante nesse canal e marque um Administrador caso necessário.'
        )
        await interaction.followup.send(embed=embed_pagamento, view=ViewFormasPagamento())
