## Async Programming With Asyncio and Workers

## What is diff b/w queue.get() and queue.getnowait() ?
`queue.get()` will get if a queue has any item and will remove the item from the queue, if the queue is empty then it will create a future and add to _getters list in the asyncio.Queue() implementation. When a queue has an element the future object from the _getters is picked, the item is added into it and the value will be returned.

It does not throw any error when the queue is empty.

`queue.getnowait` will get an item if the queue has it but it will not wait like `queue.get()` it will throw an error. We will have to handle the next steps when a queue is empty weather we retry or we send a message.

### How Workers share a common queue ?
Multiple workers can be scheduled on the event loop and a common global queue can be passed to them from which each worker will pick a task and remove that task from the queue, decreasing the queue size.

### What happens if a queue is full and we do `queue.put()` ?
If the queue is full then `queue.put()` will create a future and the future will be added to _putters in the `asycio.Queue()` implementation. When the queue has space the future with the value from the _putters will be picked and will be inserted in the queue.

### What is maxsize argument and how it is used when initializing an `asyncio.Queue(maxsize=10)` object ? 
It helps in initializing a queue which will have specific capacity, if we try to push items and if the queue has reached the maxsize then then the item has to wait until queue has some space.

It helps in handling memory overflow and backpreassure. If there is no limit to the queue size then the queue will accept items until it overflows the system memory causing errors, shutdowns and failures.

### What is Backpreassure ?
Backpreassure is a flow mechanism where a downstream component signals upstream to reduce speed when it can't keep up. In asyncio we implement it using `maxsize` parameter when queue hits limit, `await queue.put()` will pauses the producer until consumer frees space. This prevents memory overflow and provides graceful degradation.

```
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
    queue = asyncio.Queue(maxsize=3)

    await asyncio.gather(fast_producer(queue), slow_consumer(queue))

asyncio.run(main())
```

- In the above code the producer is designed to send 10 items per second.
- The consumer is designed to consume 2 items per second from the queue.
- This creates a backpreassure on the consumer if not handled, meaning the consumer will be slow while producer will fill way faster.
- To control this we will use maxsize=3 on the queue, now the producer cannot just go on filling the queue as it has to wait when the queue already has 3 items, when the consumer will consume and make space only then the producer can push items to the queue.
- So per second producer will only be able to push 2 items.
- So this creates a backpreassure that paces the producer to match the consumer's speed.

### Types of Backpreassure
1. Implicit (asyncio.Queue) - `await queue.put(item)` automatically pauses when the queue is full.
2. Explicit (HTTP 429) - API rate limiting too many requests, can retry after a set limit of seconds.
3. Reactive (TCP) - Receiver says my buffer is full, stop sending. Sender slows down automatically. The downstream controls the upstream automatically.
4. Proactive - Upstream adapts based on feedback `if queue size is > 10 then slow down, if queue.size is < 3 speed up`

