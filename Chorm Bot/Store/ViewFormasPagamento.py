
#IMPORTAÇÕES
import discord
import config

# FORMAS DE PAGAMENTO (Sem necessidade de alteração)

### VIEW QUE CONTÉM CONTÉUDO DE PAGAMENTO (from pagamento import ViewFormasPagamento)
class ViewFormasPagamento(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(QrCode())
        self.add_item(ChavePix())



# QR CODE BOTÃO
class QrCode(discord.ui.Button):
    def __init__(self):
        super().__init__(emoji='<:qrcode2:1299987136690257960>',label='Qr Code', style=discord.ButtonStyle.green)
    async def callback(self, interaction: discord.Interaction):
        
        # Gera o Embed
        embed = discord.Embed(title=f'{config.QR_CODE_EMOJI} QR CODE pagamento')
        embed.set_image(url=config.URL_QR_CODE)
        

        # Se desativa após uma vez ativado
        self.disabled = True
        await interaction.response.edit_message(view=self.view)

        # Retorna o Embed
        await interaction.followup.send(embed=embed)



# CHAVE PIX BOTÃO
class ChavePix(discord.ui.Button):
    def __init__(self):  
        super().__init__(emoji=config.CHAVE_PIX_EMOJI, label= 'Chave Aleatória', style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):

        # Se auto desativa
        self.disabled = True
        await interaction.response.edit_message(view=self.view)

        # Envia a chave PIX
        await interaction.followup.send(config.CHAVE_PIX)
        

