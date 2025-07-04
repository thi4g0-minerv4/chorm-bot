
import discord
import config  # certifique-se que o config está corretamente importado

class BotaoVerificar(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Verificar", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        cargo = guild.get_role(config.VERIFICADO_ROLE_ID)

        if not cargo:
            await interaction.response.send_message("❌ Cargo de verificação não encontrado.", ephemeral=True)
            return

        if cargo in interaction.user.roles:
            await interaction.response.send_message(
                "Você já está verificado 😊! Que tal dar uma olhada nos nossos produtos?",
                ephemeral=True
            )
            return

        await interaction.user.add_roles(cargo)
        await interaction.response.send_message("✅ Usuário verificado com sucesso!", ephemeral=True)


class ViewVerificar(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(BotaoVerificar())
