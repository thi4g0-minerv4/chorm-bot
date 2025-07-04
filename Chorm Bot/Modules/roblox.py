import aiohttp
import requests

async def get_roblox_profile(username):
    url = f"https://users.roblox.com/v1/users/search?keyword={username}&limit=10"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data['data']:
                    user_data = data['data'][0]
                    profile_info = {
                        'id': user_data['id'],
                        'name': user_data['name'],
                        'display_name': user_data['displayName'],
                        'description': user_data.get('description', 'Sem descrição disponível')
                    }
                    return profile_info
                else:
                    return "Usuário não encontrado."
            else:
                return "Erro ao acessar a API."


async def get_roblox_avatar(user_id):
    avatar_url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=720x720&format=Png"
    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as response:
            if response.status == 200:
                data = await response.json()
                if data['data']:
                    return data['data'][0]['imageUrl']
    return None

def get_roblox_gamepass(gamepass_id):
    url = f'https://apis.roblox.com/game-passes/v1/game-passes/{gamepass_id}/product-info'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()  # Retorna os dados
    except requests.exceptions.RequestException as e:
        print(f'Ocorreu um erro: {e}')
        return None
    except KeyError:
        print('A chave "PriceInRobux" não foi encontrada no JSON.')
        return None