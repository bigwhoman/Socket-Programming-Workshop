import asyncio

class CounterUDPServer:
    def __init__(self):
        self.counter = 0

    async def send_counter(self, addr):
        self.counter += 1
        next_value = self.counter
        await asyncio.sleep(0.5)
        print(f"sending {next_value} to {addr}")
        self.transport.sendto(str(next_value).encode(), addr)

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print(f"got {data.decode()} from {addr}")
        if data.decode() != "get":
            return
        loop = asyncio.get_event_loop()
        loop.create_task(self.send_counter(addr))

async def run_server():
    loop = asyncio.get_running_loop()
    await loop.create_datagram_endpoint(
        lambda: CounterUDPServer(),
        local_addr=('127.0.0.1', 12345)
    )
    print(f"Listening on 127.0.0.1:12345")
    while True:
        await asyncio.sleep(3600)

asyncio.run(run_server())