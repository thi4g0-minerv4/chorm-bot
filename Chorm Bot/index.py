
import config
import asyncio
from Modules.database import produtos_collection
from Modules.generalfunctions import url_imagem_valida
from Modules.embeds import *
from Modules.dbfunctions import reset_produtos
###IMPORTAÇÕES
import discord
from discord.ext import commands
from discord import app_commands
#IMPORTAÇÕES CLASSES
from Store.ModalCadastrarProdutos import ModalCadastrarProdutos
from Store.ViewOnOffPause import ViewBotoesOnOffPause
from Views.verificar import ViewVerificar


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)



@bot.event
async def on_ready():
    guild = bot.get_guild(config.GUILD_ID)
    # ========== CONFIGURAÇÃO GERAL DO BOT ==========
    await bot.tree.sync()  # Sincroniza Slashs
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("na Chorm Store"))  # Define status e atividade do bot

    # ====== IDENTIFICAÇÃO DA GUILDA ======
    if guild:
        print(f"Guilda encontrada: {guild.name}")  # Sucesso ao encontrar a guilda
    else:
        print("Guilda NÃO encontrada, verifique o arquivo config.py")  # Aviso caso a guilda não esteja em cache

    # ====== ON/OFF/PAUSE ======

    channel = bot.get_channel(config.ONOFF_CHANNEL_ID)
    
    await channel.purge(limit=20)  # Limpa mensagens antigas
    await channel.send(embed=config.EMBED_ON_OFF_PAUSE, view=ViewBotoesOnOffPause())  # Envia o embed com os botões de controle de status

    # ====== STORE: RESET DA VITRINE DOS PRODUTOS ======
    await reset_produtos(bot)  # Função em dbfunctions.py

    # ====== VERIFICAR ======
    channel = bot.get_channel(config.VERIFICAR_CHANNEL_ID)

    await channel.purge(limit=20)  # Limpa mensagens antigas
    await channel.send(embed=embed_verificar(), view=ViewVerificar())


    print('Tudo pronto')  # Pré sets feitos!


@bot.event 
async def on_member_join(member: discord.Member):
    channel = discord.utils.get(member.guild.text_channels, id= config.BEMVINDO_CHANNEL_ID)
    await channel.send(f'{member.mention}' , embed=embed_bem_vindo(member))


@bot.tree.command(name='cadastrar_produto')
@app_commands.choices(busca_user_roblox=[
    app_commands.Choice(name='sim', value='True'),
    app_commands.Choice(name='não', value=''),  # Mudança aqui para usar 'False' no lugar de uma string vazia
])
@app_commands.choices(quantidade_produtos=[
    app_commands.Choice(name='1 produto', value=1),
    app_commands.Choice(name='2 produtos', value=2),
    app_commands.Choice(name='3 produtos', value=3),
    app_commands.Choice(name='4 produtos', value=4),
    app_commands.Choice(name='5 produtos', value=5),
    app_commands.Choice(name='+ de 5 produtos', value=10)
])
@app_commands.choices(pronome_produto=[
    app_commands.Choice(name='Masculino', value='o'),
    app_commands.Choice(name='Feminino', value='a'),
])
async def cadastrar_produto(interaction: discord.Interaction, nome_produto: str, categoria: discord.CategoryChannel, nome_canal: str, emoji: str, busca_user_roblox: app_commands.Choice[str], url_vitrine: str, quantidade_produtos: app_commands.Choice[int], pronome_produto: app_commands.Choice[str], cor_hex_opcional:str = None):

    if interaction.user.guild_permissions.administrator:

        if produtos_collection.find_one({'nome_produto': nome_produto.lower().strip()}):
            await interaction.response.send_message(f"O produto {nome_produto} já existe no Banco de Dados. Para modificá-lo, utilize a estrutura já existente", ephemeral=True)
            return
        
        if len(nome_produto) > 25:
            await interaction.response.send_message(f"O nome do produto deve possuir menos de 25 caracteres", ephemeral=True)
            return
        
        if len(nome_canal) > 60:
            await interaction.response.send_message(f"O nome do canal deve possuir menos de 60 caracteres", ephemeral=True)
            return            
        
        if not url_imagem_valida(url_vitrine):
            await interaction.response.send_message(f"A URL `{url_vitrine}` é inválida. Comando cancelado.", ephemeral=True)
            return
        
        modal = ModalCadastrarProdutos(bot, nome_produto, categoria, nome_canal, emoji, bool(busca_user_roblox.value), url_vitrine, quantidade_produtos.value, pronome_produto.value, cor_hex_opcional)
        await interaction.response.send_modal(modal)
        
    else:
        await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)
        return


@bot.command()
async def aprovar(ctx: commands.Context, member : discord.Member = None):
    if member == None:
        await ctx.send("Você precisa marcar o membro que realizou o pagamento corretamente.", ephemeral=True)
        await ctx.message.delete()
        return

    channel = ctx.channel

    await ctx.message.delete()
    await channel.edit(name=f'✅Compra aprovada / {member.name}')
    await channel.send(f'Parabéns, {member.mention}!! Agora você se tornou oficialmente um cliente da Chorm Store.')
    await member.send(f'Parabéns!! Sua compra na Chorm Store foi aprovada.')
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False 
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    cargocliente_id = 1069642532667007058
    cargo = discord.utils.get(ctx.guild.roles, id=cargocliente_id)
    await member.add_roles(cargo)



@bot.command()
async def say(ctx, *, text: str):
    try:
        # Divide o texto em título, descrição e os valores RGB
        title_desc, r, g, b = text.rsplit('|', 3)
        
        # Divide o título e a descrição usando o caractere especial `|`
        title, description = title_desc.split('|', 1)
        
        # Converte para inteiros
        r, g, b = int(r.strip()), int(g.strip()), int(b.strip())
        
        # Cria o embed com título, descrição e cor personalizada
        embed = discord.Embed(title=title.strip(), description=description.strip())
        embed.color = discord.Color.from_rgb(r, g, b)
        
        await ctx.send(embed=embed)
        await ctx.message.delete()
        
    except ValueError:
        await ctx.send("Por favor, use o formato: `!say título | descrição | r | g | b`")


'''      Comandos calc Valores       '''



@bot.command()
async def calc_pay(ctx, valor: float = None):
    if valor is None:
        await ctx.reply('Digite um valor, e use . como vírgula, ex: 2.32')
        return
    robux = int(valor / 0.04)  # Converte para inteiro para tirar as casas decimais
    valor_formatado = f"{valor:.2f}".replace(".", ",")
    await ctx.reply(f'Com R$ {valor_formatado} você comprará {robux} Robux em nossa loja.')

@bot.command()
async def calc_robux(ctx, robux: int = None):
    if robux is None:
        await ctx.reply('Digite a quantidade de Robux que deseja comprar.')
        return
    if robux <= 0:
        await ctx.reply('O número de Robux deve ser maior que zero.')
        return
    valor = round(robux * 0.04, 2)  # Arredonda o valor para duas casas decimais
    valor_formatado = f"{valor:.2f}".replace(".", ",")
    await ctx.reply(f'R$ {valor_formatado} para comprar {robux} Robux.')




'''     Comando Clear         '''
    


@bot.command()
@commands.has_permissions(manage_messages=True)  
async def clear(ctx: commands.Context, amount: int = None):
    if amount == None:
        await ctx.reply('Digite um número após `!clear`.')
        return


    if amount < 1 or amount > 300:
        await ctx.send("Por favor, forneça um número entre 1 e 300.")
        return
    

    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'{len(deleted)} mensagens apagadas.', delete_after=5)  


'''        Comandos de Moderação        '''

# Banir membro

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx: commands.Context, member: discord.Member= None, reason =None):
    if member == None:
        await ctx.reply ('Para executar esse comando você precisa marcar alguém')
        return
    if reason == None:
        reason = 'Razão não especificada'
    if member == ctx.author or member == bot.user:
        await ctx.reply('Você não pode banir a si mesmo ou o bot.')
        return
    if ctx.author.top_role <= member.top_role:
        await ctx.reply('Você não pode banir esse membro porque ele tem um cargo mais alto que o seu.')
        return
    else:

        await member.ban(reason=reason)
        embed = discord.Embed(title=f'{member.name} foi banido.', description=reason)
        embed.color = discord.Color.from_rgb(190, 0, 20)
        await ctx.reply(embed=embed)


# Desabnir membro
@bot.command()
@commands.has_permissions(ban_members=True) 
async def unban(ctx: commands.Context, user: str = None):
    if user == None:
        await ctx.reply ('Para executar esse comando você precisa marcar alguém')
        return
    try:

        user_id = int(user.strip('<!@>'))  # Remove caracteres de menção, se houver
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.reply(f'{user.name} foi desbanido com sucesso!')
    except discord.NotFound:
        await ctx.reply('Usuário não encontrado.')
    except discord.Forbidden:
        await ctx.reply('Não tenho permissão para desbanir esse usuário.')
    except discord.HTTPException:
        await ctx.reply('Ocorreu um erro ao tentar desbanir o usuário.')


# Expulsar membro
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx: commands.Context, member: discord.Member= None, reason =None):
    if member == None:
        await ctx.reply ('Para executar esse comando você precisa marcar alguém')
        return
    if reason == None:
        reason = 'Razão não especificada'
    if member == ctx.author or member == bot.user:
        await ctx.reply('Você não pode expulsar a si mesmo ou o bot.')
        return
    if ctx.author.top_role <= member.top_role:
        await ctx.reply('Você não pode expulsar esse membro porque ele tem um cargo mais alto que o seu.')
        return
    else:

        await member.kick(reason=reason)
        embed = discord.Embed(title=f'{member.name} foi expulso.', description=reason)
        embed.color = discord.Color.from_rgb(190, 0, 20)
        await ctx.reply(embed=embed)

@bot.command()
async def membros(ctx: commands.Context):
    total_membros_humanos = sum(1 for member in ctx.guild.members if not member.bot)
    await ctx.reply(f'O servidor já conta com {total_membros_humanos} membros!!')


@bot.command()
@commands.has_permissions(administrator = True)
async def give(ctx: commands.Context,role : discord.Role = None, member: discord.Member = None):
    if role == None:
        await ctx.reply ('Você precisa mencionar um cargo')
        return
    if member == None:
        member = ctx.author
    if role in member.roles:
        await ctx.reply (f'{member.mention} já tem o cargo {role.mention}')
    else:
        await member.add_roles(role)
        await ctx.reply (f'Cargo {role.mention} foi dado a {member.mention}')

@bot.command()
@commands.has_permissions(administrator=True)
async def ungive(ctx: commands.Context,role : discord.Role = None, member: discord.Member = None):
    if role == None:
        await ctx.reply ('Você precisa mencionar um cargo')
        return
    if member == None:
        member = ctx.author
    if role not in member.roles:
        await ctx.reply(f'{member.mention} não tem o cargo {role.mention}')
    else:
        await member.remove_roles(role)
        await ctx.reply(f'Cargo {role.mention} foi removido de {member.mention}')



### ATUALIZAÇÃO 1.2
@bot.tree.command(name='calc_pay', description='Digite o valor em dinheiro para ver quantos Robux conegue comprar em nossa loja')
async def calc_pay(interaction: discord.Interaction, valor: float = None):
    if valor is None:
        await interaction.response.send_message('Digite um valor, e use . como vírgula, ex: 2.32')
        return
    robux = int(valor / 0.04)  # Converte para inteiro para tirar as casas decimais
    valor_formatado = f"{valor:.2f}".replace(".", ",")
    await interaction.response.send_message(f'Com R$ {valor_formatado} você comprará {robux} Robux em nossa loja.')

@bot.tree.command(name='calc_robux', description='Digite o valor em robux para ver o valor que estão em nossa loja')
async def calc_robux(interaction: discord.Interaction, robux: int = None):
    if robux is None:
        await interaction.response.send_message('Digite a quantidade de Robux que deseja comprar.')
        return
    if robux <= 0:
        await interaction.response.send_message('O número de Robux deve ser maior que zero.')
        return
    
    valor = round(robux * 0.04, 2)  # Arredonda o valor para duas casas decimais
    valor_formatado = f"{valor:.2f}".replace(".", ",")
    await interaction.response.send_message(f'R$ {valor_formatado} para comprar {robux} Robux.')


@bot.tree.command(name='aprovar', description='Aprova uma compra feita em nossa loja.')
async def aprovar(interaction: discord.Interaction, membro : discord.Member):


    ##--VERIFICAR PERM ADM
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)
        return
    ##--VERIFICAR PERM ADM

    channel = interaction.channel

    
    await channel.edit(name=f'✅Compra aprovada / {membro.name}')
    await channel.send(f'Parabéns, {membro.mention}!! Agora você se tornou oficialmente um cliente da Chorm Store.')
    await membro.send(f'Parabéns!! Sua compra na Chorm Store foi aprovada.')
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False 
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    cargocliente_id = 1069642532667007058
    cargo = discord.utils.get(interaction.guild.roles, id=cargocliente_id)
    await membro.add_roles(cargo)


@bot.tree.command(name='say', description='Gera um embed personalizado.')
async def say(interact: discord.Interaction, titulo: str, descricao: str, r: int, g: int, b: int):


    ##--VERIFICAR PERM ADM
    if not interact.user.guild_permissions.administrator:
        await interact.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)
        return
    ##--VERIFICAR PERM ADM

    embed = discord.Embed(title=titulo, description=descricao)
    embed.color = discord.Color.from_rgb(r, g, b)
    
    await interact.channel.send(embed=embed)
    await interact.response.send_message('Embed criado com sucesso', ephemeral=True)





   

    






bot.run (config.TOKEN)