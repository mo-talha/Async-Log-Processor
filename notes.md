## Async Programming With Asyncio and Workers

## What is diff b/w queue.get() and queue.getnowait() ?
`queue.get()` will get if a queue has any item and will remove the item from the queue, if the queue is empty then it will create a future and add to _getters list in the asyncio.Queue() implementation. When a queue has an element the future object from the _getters is picked, the item is added into it and the value will be returned.

It does not throw any error when the queue is empty.

`queue.getnowait` will get an item if the queue has it but it will not wait like `queue.get()` it will throw an error. We will have to handle the next steps when a queue is empty weather we retry or we send a message.

### How Workers share a common queue ?
Multiple workers can be scheduled on the event loop and a common global queue can be passed to them from which each worker will pick a task and remove that task from the queue, decreasing the queue size.

### What happens if a queue is full and we do `queue.put()` ?
If the queue is full then `queue.put()` will create a future and the future will be added to _putters in the `asycio.Queue()` implementation. When the queue has space the future with the value from the _putters will be picked and will be inserted in the queue.

### What is limit argument and how it is used when initializing an `asyncio.Queue()` object ? 

