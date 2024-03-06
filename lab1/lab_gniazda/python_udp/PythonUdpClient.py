import socket;

serverIP = "127.0.0.1"
serverPort = 9008
msg = "Żółta gęś"

msg_bytes = (300).to_bytes(4, byteorder='little')

print('PYTHON UDP CLIENT')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client.sendto(bytes(msg, 'cp1250'), (serverIP, serverPort))
client.sendto(bytes(msg_bytes), (serverIP, serverPort))




