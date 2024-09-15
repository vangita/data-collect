import asyncio
import time
import aiohttp
import json
import aiofiles

items_written = 0


async def collect(i, session, lock):
    global items_written
    url = f"https://jsonplaceholder.typicode.com/posts/{i}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            formatted_data = json.dumps(data, indent=4)

            async with lock:
                async with aiofiles.open('data.json', 'a') as json_file:
                    if items_written > 0:
                        await json_file.write(',\n')

                    await json_file.write(formatted_data)
                    items_written += 1


async def main():
    global items_written
    lock = asyncio.Lock()

    async with aiohttp.ClientSession() as session:
        async with aiofiles.open('data.json', 'w') as json_file:
            await json_file.write('[\n')

        tasks = []
        for i in range(1, 78):
            tasks.append(collect(i, session, lock))
        await asyncio.gather(*tasks)

        async with aiofiles.open('data.json', 'a') as json_file:
            await json_file.write('\n]')

start = time.perf_counter()
asyncio.run(main())
print(f"Time taken: {time.perf_counter() - start:.2f} seconds")









































