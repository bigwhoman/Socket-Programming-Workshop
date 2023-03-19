# Import socket module
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