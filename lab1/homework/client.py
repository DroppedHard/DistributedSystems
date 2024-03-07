import socket
import threading
import sys
import signal
from ascii_art import ART

stop_event = threading.Event()

def receive_tcp_messages(client_socket):
    try:
        while not stop_event.is_set():
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
    except Exception as e:
        print(f"Error receiving message: {e}")
    
    print("Stop event initiated, stopping TCP thread...")

def receive_udp_messages(socket:socket.socket):
    try:
        while True:
            data, _ = socket.recvfrom(1024)
            msg = str(data, 'utf-8')
            print(msg)
    except Exception as e:
        print("UDP thread stopped: ", e)


def sigint_handler(sig, frame):
    print("Ctrl + C pressed, exiting...")
    stop_event.set()
    client_tcp.close()
    sys.exit(1)

signal.signal(signal.SIGINT, sigint_handler)

host = '127.0.0.1'
port = 5555

client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_tcp.connect((host, port))

receive_thread = threading.Thread(target=receive_tcp_messages, args=(client_tcp,))
receive_thread.start()

receive_thread = threading.Thread(target=receive_udp_messages, args=(client_udp,))
receive_thread.start()

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