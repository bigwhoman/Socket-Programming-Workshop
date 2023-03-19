import socket
import asyncio
port = 12345
async def handle_client(client,addr):
    loop = asyncio.get_event_loop()
    loop.sock_sendall(client,'connected to server'.encode())
    request = None
    while request != 'quit':
        request = (await loop.sock_recv(client, 255)).decode('utf8')
        print(f'got from {addr} : {request}')
        response = 'got message'
        await loop.sock_sendall(client, response.encode('utf8'))
    client.close()

async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen(8)
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client, addr = await loop.sock_accept(server)
        print("connected to client :",addr)
        loop.create_task(handle_client(client,addr))

asyncio.run(run_server())