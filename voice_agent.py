"""
Evercall will be an instance of Call class
call class will have
- session_id (this will help to put llm response and tts voice into the right queues using this id)
- queue to store voice packets
- queue to store stt text
- queue to store llm text
- queue to store llm tts

- Workers
- A worker to pick the voice packet send it over to stt and put it back in the stt queue
- A worker to pick the text from stt queue send it to llm and get the response and put the response into the llm queue
- A worker to pick the llm response from llm queue send it to tts and put the tts response into the tts queue
- Finally a worker will pick the voice response from tts queue and stream it back to the user
"""
import asyncio

class Call:
    def __init__(self, session_id: int):
        self.session_id = session_id
        self.input_queue = asyncio.Queue()
        self.stt_queue = asyncio.Queue()
        self.llm_queue = asyncio.Queue()
        self.tts_queue = asyncio.Queue()
        self.response = []
        
async def input_producer(words: list, call: Call):
    for word in words:
        print(f"ℹ️ Input Producer Filling input queue of call session {call.session_id} ℹ️")
        await call.input_queue.put(word)
        await asyncio.sleep(2)

async def input_queue_processor(call: Call):
    print(f"🧑‍🏭 Input Queue Processor started, will start sending the input to STT 🧑‍🏭")
    
    input_queue = call.input_queue
    stt_queue = call.stt_queue
    
    while True:
        try:
            word = await asyncio.wait_for(input_queue.get(), timeout=6)
            await stt_queue.put(word)
            input_queue.task_done()    
        except asyncio.TimeoutError:
            print(f"🚨Input Queue Empty, Input Queue Processor Stopping for call session {call.session_id} 🚨")
            break

async def stt_queue_processor(call: Call):
    print(f"🧑‍🏭 STT Queue Processor started, will start generating LLM Response for call session {call.session_id} 🧑‍🏭")

    stt_queue = call.stt_queue
    llm_queue = call.llm_queue

    while True:
        try:
            print(f"Generating LLM Response for call session {call.session_id}")
            word = await asyncio.wait_for(stt_queue.get(), timeout=6)
            await asyncio.sleep(3)
            await llm_queue.put(word)
            stt_queue.task_done()

        except asyncio.TimeoutError:
            print(
                f"🚨STT Queue Empty, STT Queue Processor Stopping for call session {call.session_id} 🚨")
            break

async def llm_response_processor(call: Call):
    print(f"🧑‍🏭 LLM Response Processor started, will start generating voice Response for LLM Response for {call.session_id} 🧑‍🏭")

    llm_queue = call.llm_queue
    response: list = call.response
    
    while True:
        try:
            print(f"Generating voice for LLM response for call {call.session_id}")
            word = await asyncio.wait_for(llm_queue.get(), timeout=5)
            await asyncio.sleep(4)
            response.append(word)
        except asyncio.TimeoutError:
            print(f"LLM Response Queue Empty, llm_response_processor shutting down for call {call.session_id}")
            break

async def main():
    call1 = Call(1)
    
    words = ["Hi", "My", "Name", "is", "Mohammed", "Talha", "I", "am", "26", "years", "old"]

    await asyncio.gather(input_producer(words, call1), input_queue_processor(call1), stt_queue_processor(call1), llm_response_processor(call1))

    print(call1.response)
    
asyncio.run(main())