import socket
import threading
import sys
import signal
from ascii_art import ART

stop_event = threading.Event()

def receive_messages(client_socket):
    while not stop_event.is_set():
        try:
            # Receive and display messages from the server
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    
    print("Stop event initiated, stopping the thread...")

def sigint_handler(sig, frame):
    print("Ctrl + C pressed, exiting...")
    stop_event.set()
    client_tcp.close()
    sys.exit(1)

signal.signal(signal.SIGINT, sigint_handler)

# Set up the client
host = '127.0.0.1'
port = 5555

client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_tcp.connect((host, port))

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages, args=(client_tcp,))
receive_thread.start()

# Send messages to the server
try:
    while True:
        message = input()
        if message == 'U':
            client_udp.sendto(bytes(ART, 'utf-8'), (host, port))
        else:
            client_tcp.send(message.encode('utf-8'))
except KeyboardInterrupt:
    print("Ctrl + C pressed, exiting...")
finally:
    client_tcp.close()
    stop_event.set()
    sys.exit(1)
