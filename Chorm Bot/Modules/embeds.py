import discord
import config
from Modules.dbfunctions import get_dados_produto

def embed_select(produto):
    dados = get_dados_produto(produto)
    embed_select = discord.Embed(title=f'**Selecione no campo abaixo {dados['pronome_produto']} {dados['nome_produto'].capitalize()} que deseja comprar**')
    embed_select.color = discord.Color.from_rgb(255,0,0)
    embed_select.set_image(url=dados['url_vitrine'])

    return embed_select


def embed_bem_vindo(member: discord.Member):
    embed = discord.Embed(
        title=f"{config.MAIN_EMOJI} Bem-vindo ao Chorm Store! {config.MAIN_EMOJI}",
        description=f"""
🚀 **O que você pode fazer aqui:**

Explorar nossas ofertas de Robux  
Participar de promoções exclusivas  
Conversar com outros membros da comunidade  
Dúvidas? Nossa equipe está aqui para ajudar!

• Leia as <#{config.REGRAS_CHANNEL_ID}>

• Verifique-se <#{config.VERIFICAR_CHANNEL_ID}>

Aproveite a sua estadia!
""",
        color=discord.Color.from_rgb(135, 9, 0)
    )

    embed.set_thumbnail(url=member.display_avatar.url)
    return embed

def embed_verificar():
    embed = discord.Embed(title='<:Red_verified:1294327829734883330> CHORM STORE | VERIFICAÇÃO DE USUÁRIO', description=f'''Por prezarmos pela segurança e integridade de nosso usuário adquirimos a verificação para maior conforto.
                          
Vantagens:
                          
- AntiSpam, você não receberá  será perturbado com mensagens diretas
- Desbloqueiamento de canais do servidor
- Mais conforto e segurança

:dart: Clique no botão para concluir sua verificação.''',
    color= discord.Color.from_rgb(135, 9, 0)
)
    return embed

    