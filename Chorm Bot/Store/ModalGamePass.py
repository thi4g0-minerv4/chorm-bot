import discord
import config
from Modules.roblox import get_roblox_gamepass
from Store.ViewFormasPagamento import ViewFormasPagamento

class ModalGamePass(discord.ui.Modal):
    def __init__(self, nickname_roblox):
        super().__init__(title="Game Pass", timeout=None)
        self.text_input = discord.ui.TextInput(
            label="Envie o Link da sua GamePass", 
            placeholder="Ex: https://www.roblox.com/pt/game-pass/88985/vip-50-off"
        )
        self.add_item(self.text_input)
        self.nickname_roblox = nickname_roblox

    async def on_submit(self, interaction: discord.Interaction):
        
        gamepass_id = self.text_input.value.split('/')[-2]
        profile = get_roblox_gamepass(gamepass_id)

        if profile is not None:
            robux = profile.get('PriceInRobux', 'Preço não encontrado') / 100 * 70
            preco = robux * 0.04 # Preço dos robux
            preco_formatado = "{:.2f}".format(preco)  # Limita para 2 casas decimais
            preco_br = preco_formatado.replace('.', ',')  # Substitui o ponto por vírgula


            embed = discord.Embed(title=f'<:Red_verified:1294327829734883330> Pedido de {interaction.user.name}', description=f'''
Está quase lá, para **avançarmos** com a venda, selecione o **método de pagamento abaixo.**
''')
            embed.add_field(name=f'{config.ROBLOX_EMOJI} Roblox Nick:',value=f"{self.nickname_roblox}", inline=True)

            embed.add_field(name=f'{config.MONEY_EMOJI} Valor Final:',value=f"R$ {preco_br}", inline=True)

            embed.add_field(name=f'{config.ROBLOX_EMOJI} Quantidade de Robux:',value=f"{int(robux)} Robux", inline=True) # 30% de taxa



            embed.color = discord.Color.from_rgb(255,0,0)
            

            embed1 = discord.Embed(description=f'''Para o cliente receber os Robux, usamos o método de Gamepass a onde você precisa possuir uma, caso não tenha assista o video abaixo.

**Video Tutorial** : https://www.youtube.com/@ChormStore/videos
**Valor da Gamepass** : {int(robux)} Robux''')
            embed1.color = discord.Color.from_rgb(255,0,0)



            embed2 =discord.Embed(title='Escolha sua forma de pagamento')
            embed2.set_footer(text='Após a compra envie o comprovante.')
            embed2.color = discord.Color.from_rgb(255,0,0)

            await interaction.response.send_message( embed=embed)
            await interaction.channel.send(embed=embed1, view=ViewFormasPagamento())
            
            await interaction.message.delete()

        else:
            await interaction.response.send_message('Game Pass não encontrado, insira novamente.')

