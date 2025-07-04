# Modules/database.py

# ===== IMPORTS =====
import config
from pymongo import MongoClient


# ===== CONEXÃO COM O MONGODB =====
client = MongoClient(config.CLIENT)   # URI de conexão (vinda do config)
db = client[config.DB]                # Seleciona o banco de dados principal


# ===== COLEÇÕES DO BANCO =====
produtos_collection = db[config.PRODUTOS_COLLECTION]
loja_collection = db[config.LOJA_COLLECTION]