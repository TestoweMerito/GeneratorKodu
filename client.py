import socket
import struct
from generated import messages

HOST = '127.0.0.1'
PORT = 9000

def recv_all(sock, n):
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError('socket closed')
        data += chunk
    return data

def recv_msg(sock):
    raw_len = recv_all(sock, 4)
    (length,) = struct.unpack('<I', raw_len)
    return recv_all(sock, length)

def send_msg(sock, data):
    sock.sendall(struct.pack('<I', len(data)) + data)

def main():
    with socket.create_connection((HOST, PORT)) as s:
        greeting = messages.Greeting(
            id=123,
            message='Cześć serwerze',
            value=3.14,
            flags=True,
            payload=b'bin payload',
            numbers=[1,2,3,4]
        )
        send_msg(s, greeting.to_bytes())
        reply = recv_msg(s)
        resp = messages.Response.from_bytes(reply)
        print('Server replied:', resp.__dict__)

if __name__ == '__main__':
    main()
