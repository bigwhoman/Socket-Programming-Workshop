import asyncio
import asyncudp
port = 12345
async def run_client():
    sock = await asyncudp.create_socket(remote_addr=("127.0.0.1", port))
    for _ in range(10):
        sock.sendto(b'get')
        print("set the get message")
        data, addr = await sock.recvfrom()
        print(f"got {data.decode()} from {addr}")
        await asyncio.sleep(0.5)
    sock.close()

asyncio.run(run_client())