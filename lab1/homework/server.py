import socket
import threading
import sys
import signal


stop_event = threading.Event()

def sigint_handler(sig, frame):
    print("Ctrl + C detected, exiting...")
    stop_event.set()
    server_tcp.close()
    sys.exit(1)

signal.signal(signal.SIGINT, sigint_handler)

# Function to handle client connections
def handle_client(client_socket, addr, client_id, clients):
    while not stop_event.is_set():
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f"Client {addr} disconnected")
                clients.remove(client_socket)
                break

            # Broadcast the message to all connected clients
            data = f"{client_id}: " + data
            for client in clients:
                if client != client_socket:
                    client.send(data.encode('utf-8'))
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            clients.remove(client_socket)
            break
    
    print(f"Ending client {client_id} thread")

def send_dying_message(clients):
    message = "Server down. Communication is not possible"
    for client in clients:
        client.send(message.encode('utf-8'))

# Set up the server
host = '127.0.0.1'
port = 5555

server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_tcp.bind((host, port))
server_tcp.listen(5)

server_udp.bind(('', port))
buff = []

def handle_udp():
    while not stop_event.is_set():
        try:
            buff, address = server_udp.recvfrom(1024)
            print("received: " + str(buff, 'utf-8'))
        except KeyboardInterrupt:
            break
    
    print("UDP thread stopped")

print(f"Server listening on {host}:{port}")

clients = []
client_id = -1
# Accept and handle client connections
try:
    while True:
        # udp_thread = threading.Thread(target=handle_udp, args=())
        client_socket, addr = server_tcp.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        client_id += 1
        clients.append(client_socket)
        
        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, client_id, clients))
        # client_thread.daemon = True
        client_thread.start()
except socket.error as e:
    print("Server socket error: ", e)
except KeyboardInterrupt:
    print("Ctrl + C detected, exiting...")
finally:
    send_dying_message(clients)
    stop_event.set()
    server_tcp.close()
    print("Server going down...")
    sys.exit(1)

