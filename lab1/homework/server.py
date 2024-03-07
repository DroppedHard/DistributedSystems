import socket
import threading
import sys
import signal
from concurrent.futures import ThreadPoolExecutor


stop_event = threading.Event()
executor = ThreadPoolExecutor(5)

def sigint_handler(sig, frame):
    print("Ctrl + C detected, exiting...")
    stop_event.set()
    server_tcp_socket.close()
    sys.exit(1)

signal.signal(signal.SIGINT, sigint_handler)

def handle_tcp_message(addr, client_id):
    client_socket = clients[client_id]
    while not stop_event.is_set():
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f"Client {addr} disconnected")
                clients.pop(client_id)
                break

            data = f"{client_id}: {data}"
            for id in clients.keys():
                if id != client_id:
                    clients[id].send(data.encode('utf-8'))
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            clients.pop(client_id)
            break
    
    print(f"Ending client {client_id} thread")

host = '127.0.0.1'
port = 5555

server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_tcp_socket.bind((host, port))
server_tcp_socket.listen(5)

server_udp_socket.bind(('', port))
buff = []

def handle_udp_message(socket:socket.socket):
    while not stop_event.is_set():
        try:
            buff, client_addr = socket.recvfrom(1024)
            print("Sending ASCII art: " + str(buff, 'utf-8'))
            for addr in address_to_id.keys():
                if addr != client_addr:
                    socket.sendto(buff, addr)
        except KeyboardInterrupt:
            socket.close()
            stop_event.set()
            break
    
    print("UDP thread stopped")

executor.submit(handle_udp_message, server_udp_socket)

print(f"Server listening on {host}:{port}")

clients:dict[int, socket.socket] = {}
client_id = -1
address_to_id = {}
try:
    while True:
        client_socket, addr = server_tcp_socket.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        client_id += 1
        clients[client_id] = client_socket
        address_to_id[addr] = client_id

        executor.submit(handle_tcp_message, addr, client_id)
except socket.error as e:
    print("Server socket error: ", e)
except KeyboardInterrupt:
    print("Ctrl + C detected, exiting...")
finally:
    stop_event.set()
    server_tcp_socket.close()
    print("Server going down...")
    sys.exit(1)