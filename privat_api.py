import aiohttp
from config import BASE_API_URL


async def get_exchange_archive(session: aiohttp.ClientSession, date: str):
    url = f"{BASE_API_URL}exchange_rates?json&date={str(date)}"
    try:
        async with session.get(url) as response:
            body = await response.json()
            print(f"Status: {response.status} for url {url}")
            return body
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))
