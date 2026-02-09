import asyncio

urls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

task_q = asyncio.Queue()
result_q = asyncio.Queue()

async def worker(q: asyncio.Queue):
    url = q.get_nowait()
    asyncio.sleep(3)
    result_q.put_nowait(url)

[asyncio.create_task(worker(task_q)) for _ in range(5)]