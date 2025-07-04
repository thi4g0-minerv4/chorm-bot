import discord
import asyncio
from Modules.roblox import *
from Store.ViewVerifyRobloxProfile import ViewVerifyRobloxProfile

class ModalInsiraNickname(discord.ui.Modal):
    def __init__(self, nome_produto_formatado):
        super().__init__(title="Insira seu NickName", timeout=None)
        self.nome_produto = nome_produto_formatado

        self.text_input = discord.ui.TextInput(label="Digite seu NickName", placeholder="Ex: wolfzinbr123...")
        self.add_item(self.text_input)


    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        
        
        username = self.text_input.value
        profile = await get_roblox_profile(username)

        if isinstance(profile, dict):
            await interaction.message.delete()
            id_roblox = profile['id']
            avatar_roblox = await get_roblox_avatar(id_roblox)  
            nickname_roblox = profile['name']
            descricao_roblox = profile['description']

            url_roblox = f'https://www.roblox.com/users/{id_roblox}/profile'

            embed = discord.Embed(title="Verifique se esse é seu perfil")
            embed.add_field(name="Nome de usuário", value=nickname_roblox, inline=False)
            embed.add_field(name="ID", value=id_roblox, inline=False)
            embed.add_field(name="Descrição", value=descricao_roblox, inline=False)
            embed.add_field(name="Link do perfil", value=url_roblox, inline=False)
            embed.color = discord.Color.from_rgb(255, 0, 0)

            if avatar_roblox:
                embed.set_thumbnail(url=avatar_roblox)

            
            await interaction.followup.send(
                embed=embed,
                view=ViewVerifyRobloxProfile(self.nome_produto, nickname_roblox, url_roblox)
            )

        else:
            message = await interaction.followup.send(
                'A API do roblox não consegue buscar diversos perfis ao mesmo tempo, provavelmente ela está sobrecarregada agora, tente de novo em alguns segundos ou minutos.',
                ephemeral=True
            )
            await asyncio.sleep(3)
            await message.delete()
