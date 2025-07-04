# Modules/generalfunctions.py

# ===== IMPORTS =====
import config
from discord.ext import commands
import requests
import discord
# ===== DATABASE =====
# ===== MODULES =====

# ===== FUNÇÕES =====

def formatar_produto(produto: str):
    return produto.lower().strip()

# ----------------------- Validar Url de imagem (cadastrar_produtos) -----------------------
def url_imagem_valida(url):
    try:
        resp = requests.head(url, timeout=5)
        if resp.status_code == 200:
            content_type = resp.headers.get('Content-Type', '')
            return content_type.startswith('image/')
        return False
    except Exception:
        return False


