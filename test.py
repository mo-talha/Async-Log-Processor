# import asyncio
# import random

# async def producer(urls: list, task_queue: asyncio.Queue):
#     for url in urls:
#         await task_queue.put(url)  # PUT FIRST!
#         print(f"adding {url} to task queue")
#         await asyncio.sleep(1)  # Sleep AFTER putting

# async def worker(worker_id, q: asyncio.Queue, result_q: asyncio.Queue):
#     """Worker that processes ALL available items"""
#     print(f"Worker {worker_id} started")
#     messages = ["200", "404"]

#     # Process until queue is empty
#     while True:
#         try:
#             url = await asyncio.wait_for(q.get(), timeout=5)
#             print(f"Worker {worker_id} fetching {url}")
#             await asyncio.sleep(5)

#             await result_q.put(
#                 {
#                     "url": url,
#                     "message": random.choice(messages)
#                 }
#             )
#             print(f"Worker {worker_id} success {url}")
#             q.task_done()
#         except asyncio.TimeoutError:
#             print(f"worker {worker_id} could not get an item from the task queue")
#             break
    
# async def result_queue_processor(result_q: asyncio.Queue):
#     while True:
#         try:
#             message = await asyncio.wait_for(result_q.get(), timeout=10)
#             if message["message"] == "404":
#                 print(f"🚨 ALERT 404: {message['url']}")
#             else:
#                 print(f"✅ OK 200: {message['url']}")
#             result_q.task_done()
#         except asyncio.TimeoutError:
#             print("⏰ Result queue empty for 5s, shutting down")
#             break
            
# async def main(): 
#     urls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

#     # Create workers (2 of them)
#     task_queue = asyncio.Queue()
#     result_queue = asyncio.Queue()
    
#     workers = [worker(i, task_queue, result_queue) for i in range(2)]

#     # Run producer and workers concurrently
#     await asyncio.gather(producer(urls, task_queue), *workers, result_queue_processor(result_queue))

#     # Wait for any remaining tasks
#     await task_queue.join()
#     await result_queue.join()

#     print("\n✅ All done!")

# asyncio.run(main())

import asyncio

# producer which produces the links and adds to the task_q
async def producer(urls:list, task_q: asyncio.Queue):
    for url in urls:
        await task_q.put(url)
        await asyncio.sleep(1)
        
# worker or consumer which picks the link scrapes the data and puts the result in the result_q
async def worker(worker_id:int, task_q: asyncio.Queue, result_q: asyncio.Queue):
    print()
# result_processor process the result and raises alerts if something is wrong

# main method to start this whole process