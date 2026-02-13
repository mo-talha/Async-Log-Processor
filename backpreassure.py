import asyncio

async def fast_producer(queue: asyncio.Queue):
    i = 0
    
    while True:
        print(f"📤 Producer: Trying to send item {i}")
        
        await queue.put(f"item-{i}")

        print(f"Producer: sent item {i}")

        i+=1

        await asyncio.sleep(0.1)

async def slow_consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        print(f"   📥 Consumer: Got {item}")

        await asyncio.sleep(0.5)

        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=0)

    await asyncio.gather(fast_producer(queue), slow_consumer(queue))

asyncio.run(main())
