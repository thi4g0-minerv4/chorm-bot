# Chorm Bot - Loja de ROBUX

Bem-vindo à **Chorm Store**, o projeto é um bot para Discord criado para gerenciar compras de moedas virtuais (ROBUX) diretamente no servidor da Chorm, oferecendo comandos simples e funcionais para os usuários interagirem e realizarem transações.

---

## ✅ Estado Atual do Código (2.25)

> **O código atual é uma atualização da versão 2.0**, que aprimora o sistema originalmente feito para funcionalidade imediata. Atualmente o seguinte já foi incluído:

- ❌ **Ainda não utiliza estrutura com Cogs (Próxima Atualização 2.3)**
- ✅ **Possui sistema de banco de dados (Mongo DB)**
- ✅ **Possui a melhor estrutura possível, com Modules e config gerais do projeto**
- ✅ É funcional e serve como base para testes e expansão futura

---

## 📦 2.25 - O que foi incluído:


Sobre a v2.25
```
A próxima versão será uma **reforma completa**, mantendo a funcionalidade anterior, sem adições, apenas melhorias de código, e tratamento de erros/bugs. Abaixo o que será implementado:
```
### ✅ Adições/Alterações da 2.25

- 🧠 **Orientação a Banco de Dados**  
  Integração completa com MongoDB, armazenando informações de usuários, compras, saldo, histórico, também sendo possível configurar os produtos manualmente posteriormente.

- ⚙️ **Pasta de Configuração**  
  Arquivo `config.py` dedicado ao controle de:
  - Token do bot
  - Prefixo de comandos
  - Cores e emojis
  - Canais e IDs padrões
  - Taxas e regras do sistema de ROBUX
  - Gerenciar o preço atual (Facilitando promoções, aonde basta mudar 1 linha de código e pronto)

- 📦 **Pasta de Modules**  
  Lógica separada da interface (comandos). Ex: buscar produtos no DB, formatar valor em R$, funções complementares de comandos etc...

- 📦 **Pasta de Classes**  
   Views em POO, que carregam os botões, selects e modals. Tudo separado por arquivo.
----

## ✅ 2.3 - O que será adicionado:

- ✅ Tudo separado em Cogs

## Última adição: Reorganização e correção de erros no comando Cadastrar Produtos
## Versão atual: 2.25 (sendo trabalhada: 2.5)
