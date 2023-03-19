# Socket-Programming-Workshop
Socket Programming Workshop with Python and Asyncio -- Computer Networks 40443 - Spring 2023 
# What Is Socket Programming
Directly connecting two nodes in the network.
# What is asyncio
asyncio is a library to write concurrent code using the async/await syntax.<br>
asyncio is often a perfect fit for IO-bound and high-level structured network code.
# Eagle Eye view of what we are doing
We will create multiple client and a server and first try to connect the clients to our server.

![](https://files.realpython.com/media/sockets-tcp-flow.1da426797e37.jpg)
# Getting to Work
## Installing the requirements
First, Clone the project. Then, proceed to the root directory and run the command below.<br>
To install the required packages run : 
```shell
python -m pip install -r requirements.txt
```
## Server without asyncio
Code copied from geeksForGeeks
### server.py
```python
import socket # for socket
import sys
 
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))
 
# default port for socket
port = 80
 
try:
    host_ip = socket.gethostbyname('www.google.com')
    print ("host ip is :",host_ip)
except socket.gaierror:
 
    # this means could not resolve the host
    print ("there was an error resolving the host")
    sys.exit()
 
# connecting to the server
s.connect((host_ip, port))
 
print ("the socket has successfully connected to google")
```

Now we bind the socket to a port :

### server2.py
```python
# first of all import the socket library
import socket            
 
# next create a socket object
s = socket.socket()        
print ("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345               
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(5)    
print ("socket is listening")           
 
# a forever loop until we interrupt it or
# an error occurs
while True:
 
# Establish connection with client.
  c, addr = s.accept()    
  print ('Got connection from', addr )
 
  # send a thank you message to the client. encoding to send byte type.
  c.send('Thank you for connecting'.encode())
 
  # Close the connection with the client
  c.close()
   
  # Breaking once connection closed
  break
```

And now to test our program : 
### client
```ps
PS C:\Users\VivoBook> ncat localhost 12345
libnsock ssl_init_helper(): OpenSSL legacy provider failed to load.

Thank you for connecting
```
### server
```cmd
Socket successfully created
socket binded to 12345
socket is listening
Got connection from ('127.0.0.1', 35429)
```

Now we add multiple read feature : 
### server3.py
```python
# first of all import the socket library
import socket            
 
# next create a socket object
s = socket.socket()        
print ("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345               
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(5)    
print ("socket is listening")       

# add the buffer size for receiving and sending messages    
buff_size = 1500

# a forever loop until we interrupt it or
# an error occurs
while True:
 
# Establish connection with client.
  c, addr = s.accept()    
  print ('Got connection from', addr )
 
  # send a thank you message to the client. encoding to send byte type.
  c.send('Thank you for connecting\n'.encode())
  while True : 
    received_message = c.recv(buff_size).decode()
    print("got message from client :",received_message)
    c.send('got your message'.encode())
    if 'quit' in received_message :
        print("quiting ...")
        break
  # Close the connection with the client
  c.close()
  break 
    
```
### client
```ps
PS C:\Users\VivoBook> ncat localhost 12345
libnsock ssl_init_helper(): OpenSSL legacy provider failed to load.

Thank you for connecting
hello world
quit
```
### server
```cmd
Socket successfully created
socket binded to 12345
socket is listening
Got connection from ('127.0.0.1', 36725)
hello world

quit

quiting ...

```

Now we create a client app to connect to our server
### client.py
```python
import socket        
# Define the buffer in which the answers are got    
buff_size = 1500
# Create a socket object
s = socket.socket()        
 
# Define the port on which you want to connect
port = 12345               
 
# connect to the server on local computer
s.connect(('127.0.0.1', port))
s.send('ack'.encode()) 
print(s.recv(buff_size).decode())
# receive data from the server and decoding to get the string.
while True :
    send_message = input()
    s.send(send_message.encode())
    if send_message == 'quit' :
        break
    received_message = s.recv(buff_size).decode()
    print("got message from server :",received_message)
# close the connection
s.close() 
```
## tests
### client
```cmd
Workshop>python ./codes/client.py
Thank you for connecting

hello world
got message from server : got your message
```
### server
```cmd
Workshop>python ./codes/server3.py
Socket successfully created
socket binded to 12345
socket is listening   
Got connection from ('127.0.0.1', 38465)
got message from client : ack
got message from client : hello world
```
# Async Connection Handling
Now the problem is that the previous connection is blocking and the server can't simultaniously listen and answer to multiple connections. This is the part where asyncio comes in place.

### async_server.py
```python
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
```
Now we test 
### server
```cmd
got from ('127.0.0.1', 41046) : ack
connected to client : ('127.0.0.1', 41052)
got from ('127.0.0.1', 41052) : ack
got from ('127.0.0.1', 41046) : hello world
got from ('127.0.0.1', 41052) : how are you
```
### client
```cmd 
python ./codes/client.py
got message
how are you
got message from server : got message
```
### client
```cmd
python ./codes/client.py
got message
hello world
got message from server : got message
```
# UDP Socket
So far we have only used tcp sockets, what if we want to communicate with a udp socket ?<br>
The challenging part is that the server does not know the source which the packets come from.
### server
```python
import asyncio
port = 12345
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
        local_addr=('127.0.0.1', port)
    )
    print(f"Listening on 127.0.0.1:{port}")
    while True:
        await asyncio.sleep(3600)

asyncio.run(run_server())
```
### client
```python
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
```
# Appendix
### socket.socket(socket.AF_INET, socket.SOCK_STREAM)
creates a socket with two parameters : (1) Protocol - (2) Socket Type
### AF_INET     
Address Family = IPv4
### SOCK_STREAM 
The type of socket is tcp stream
### socket.bind(('', port)) 
Bind socket to the port of every address
### socket.accept
Waits for a connection to establish and then returns the connection and address of connection<br>
### socket.listen(num)
Puts the socket into listening mode<br>
### socket.setblocking(False)
Makes the socket non-blocking (as expected)<br>
### asyncio.get_event_loop()
Creates an event loop which can then run async tasks<br>
### loop.create_task(self.send_counter(addr))
Runs an async task<br>
### asyncio.run(run_client())
Like create task but mostly used for the main function<br>
### loop.sock_sendall(connection,'message'.encode())
Sends message through a socket <br>
### await loop.create_datagram_endpoint( lambda: CounterUDPServer(),local_addr=('127.0.0.1', port))
Creates an endpoint and listens to it