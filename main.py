import asyncio
import logging
import sys
import time
from copy import copy
from pprint import pprint

from aiohttp import ClientSession

from config import DEFAULT_CURRENCIES
from data_conversion import adapt_exchange_json
from date_utils import get_date_in_past
from privat_api import get_exchange_archive


async def main():
    args_length = len(sys.argv)
    days_back = abs(int(sys.argv[1]))
    currencies = copy(DEFAULT_CURRENCIES)
    if args_length >= 3:
        currencies.extend(sys.argv[2:])
    if days_back > 10:
        logging.debug(f"The maximum number of days for getting rates is 10")
        return
    privat_calls = []
    async with ClientSession() as session:
        for i in range(days_back):
            past_date = get_date_in_past(i + 1)
            privat_calls.append(
                get_exchange_archive(session=session, date=past_date)
            )
        responses = await asyncio.gather(*privat_calls)
        adapted_responses = adapt_exchange_json(rates=responses, currencies=currencies)
        return adapted_responses


if __name__ == "__main__":
    start_time = time.time()
    results = asyncio.run(main())
    pprint(results)
    duration = time.time() - start_time
    pprint(f"{duration = }")


