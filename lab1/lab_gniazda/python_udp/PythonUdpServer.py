import socket;

serverPort = 9009 # listening pingport
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort))
buff = []

print('PYTHON UDP SERVER')

while True:

    buff, address = serverSocket.recvfrom(1024)
    # int.from_bytes(buff, byteorder='little')
    print("python udp server received msg: " + str(int.from_bytes(buff, byteorder='little')))



