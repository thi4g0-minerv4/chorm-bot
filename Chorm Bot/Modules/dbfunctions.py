# ===== IMPORTS =====
import config
from discord.ext import commands
import discord
import asyncio

# ===== DATABASE =====
from Modules.database import produtos_collection, loja_collection

# ===== MODULES =====
from Modules.generalfunctions import formatar_produto

# ===== FUNÇÕES DE PRODUTO =====
def get_dados_produto(nome_produto: str) -> dict | None:
    nome_formatado = formatar_produto(nome_produto)
    return produtos_collection.find_one({"nome_produto": nome_formatado})

# ===== FUNÇÕES DE STATUS DA LOJA =====
def status_loja():
    loja = loja_collection.find_one()
    return loja["status"] if loja else "Loja não encontrada"

def ligar_loja():
    loja_collection.update_one({}, {"$set": {"status": "on"}})

def desligar_loja():
    loja_collection.update_one({}, {"$set": {"status": "off"}})

def pausar_loja():
    loja_collection.update_one({}, {"$set": {"status": "pause"}})

# ===== GERAR EMBED DA VITRINE =====
def gerar_embed_vitrine(nome_produto, bot: commands.Bot):

    match status_loja():
        case 'on':
            status = 'Aberta ✅'
        case 'off':
            status = 'Fechada ❌'
        case 'pause':
            status = 'Pausada 📢'

    embed = discord.Embed(
        title='Bem-vindo! a ⠂ CHORM STORE 🛒',
        description=(
            "Para continuar, clique em Abrir Carrinho. Na realização da compra, "
            "você deve ser objetivo e responder todas as perguntas.\n\n"
            f"🔗 ⠂ Ao pressionar o botão, você está de acordo com todos os {bot.get_channel(config.TERMOS_CHANNEL_ID).mention} "
            "e condições de nossa loja.\n\n"

            f"Status da Loja: **{status}**"
        )
    )

    result = get_dados_produto(nome_produto)
    url_vitrine = result['url_vitrine']
    cor = result['cor']

    embed.set_image(url=url_vitrine)

    # Validação básica da cor
    if not cor:  # Caso None
        embed.color = discord.Color.from_rgb(142, 38, 43)
        return embed

    caracteres_hex = set('0123456789abcdef')
    if not (cor.startswith('#') and len(cor) == 7):
        embed.color = discord.Color.from_rgb(142, 38, 43)
        return embed

    cor_clean = cor[1:].lower()
    if any(c not in caracteres_hex for c in cor_clean):
        embed.color = discord.Color.from_rgb(142, 38, 43)
        return embed

    embed.color = discord.Color.from_str(cor)
    return embed

# ===== GERAR EMBED STATUS =====
def embed_status(interaction: discord.Interaction):
    status = status_loja()

    if status == "on":
        embed = discord.Embed(
            title=':bell: **Loja Aberta**',
            description=(
                "Confira já a Loja e garanta logo seus *PRODUTOS*,\n"
                "Vendemos em todos os jogos desde que tenha sistema de *GIFT* :gift:\n\n"
                "Corra antes que acabe"
            )
        )
        embed.color = discord.Color.from_rgb(51, 255, 65)

    elif status == "off":
        embed = discord.Embed(
            title=':bell: Loja Fechada',
            description=(
                "Agradecemos a todos clientes que adquiram produtos da loja hoje!\n\n"
                f"A loja será ABERTA AMANHÃ, confira os horários aproximados em {interaction.guild.get_channel(config.HORARIO_CHANNEL_ID).mention}\n"
            )
        )
        embed.color = discord.Color.from_rgb(255, 0, 0)

    elif status == "pause":
        embed = discord.Embed(
            title=':loudspeaker: LOJA Pausada',
            description=(
                ":alarm_clock: Estamos momentaneamente pausados até que consigamos resolver todos os **tickets** ou reabastecer o estoque.\n"
            )
        )
        embed.color = discord.Color.from_rgb(252, 198, 3)

    else:
        print('Status da loja inválido:', status)
        return None

    return embed

# ===== FUNÇÃO ASSÍNCRONA PARA RESETAR PRODUTOS NA VITRINE =====
async def reset_produtos(bot: commands.Bot):
    from Store.ViewAbrirCarrinho import ViewAbrirCarrinho

    guild = bot.get_guild(config.GUILD_ID)

    for produto in produtos_collection.find():

        canal = guild.get_channel(produto['id_canal'])
        if not canal:
            print(f'Canal do produto {produto['nome_produto'].capitalize()} não encontrado.')
            continue
        embed = gerar_embed_vitrine(produto['nome_produto'], bot)

        view = ViewAbrirCarrinho(produto['nome_produto']) if status_loja() == 'on' else None

        await canal.purge(limit=2)  # Limpa as 2 últimas mensagens

        await canal.send(embed=embed, view=view)
