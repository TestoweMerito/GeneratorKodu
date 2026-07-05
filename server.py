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

def recv_msg(conn):
    raw_len = recv_all(conn, 4)
    (length,) = struct.unpack('<I', raw_len)
    return recv_all(conn, length)

def send_msg(conn, data):
    conn.sendall(struct.pack('<I', len(data)) + data)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f'Server listening on {HOST}:{PORT}')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            try:
                while True:
                    data = recv_msg(conn)
                    if not data:
                        break
                    msg = messages.Greeting.from_bytes(data)
                    print('Received:', msg.__dict__)
                    # Echo back a Response
                    resp = messages.Response(status=0, message=f"Hello id={msg.id}")
                    send_msg(conn, resp.to_bytes())
            except ConnectionError:
                print('Connection closed')

if __name__ == '__main__':
    main()
