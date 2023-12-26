from aiofile import async_open


async def write_to_file(file_path: str, msg: str):
    async with async_open(file_path, 'a') as afp:
        await afp.write(msg + "\n")
