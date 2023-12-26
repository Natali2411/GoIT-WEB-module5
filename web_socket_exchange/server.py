import asyncio
from datetime import datetime
import json
import logging
import websockets
import names
from aiohttp import ClientSession
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

from config import DEFAULT_CURRENCIES
from privat_api import get_exchange_archive
from utils.data_conversion import get_tabulate_rate
from utils.date_utils import get_date_in_past
from utils.file_logger import write_to_file

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def send_exchange_rates(self, currencies: list[str], days_back: int = 0):
        async with ClientSession() as session:
            privat_calls = []
            for day_back in range(days_back + 1):
                past_date = get_date_in_past(days_back=day_back)
                privat_calls.append(
                    get_exchange_archive(session=session, date=past_date)
                )
            rates = await asyncio.gather(*privat_calls)
            rates_table = json.dumps(get_tabulate_rate(rates=rates, currencies=currencies))
            await self.send_to_clients(rates_table)

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            msgs = message.split()
            msgs_len = len(msgs)
            if msgs:
                if msgs[0] == "exchange":
                    log_msg = f"{datetime.now()} - Exchange command has executed with " \
                               f"parameters: " + ", ".join(msgs[1:])
                    await write_to_file(file_path="logs/exchange.txt", msg=log_msg)
                    if msgs_len == 1:
                        await self.send_exchange_rates(currencies=DEFAULT_CURRENCIES)
                    elif msgs_len > 1:
                        if int(msgs[1]) > 10:
                            await self.send_to_clients(
                                f"The maximum number of days for getting rates is 10")
                        else:
                            await self.send_exchange_rates(currencies=DEFAULT_CURRENCIES,
                                                           days_back=int(msgs[1]))
            else:
                await self.send_to_clients(f"Command '{message}' wasn't recognised")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
