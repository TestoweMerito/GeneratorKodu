import socket
from generated import messages
from generated.transport import Sender, Receiver

HOST = '127.0.0.1'
PORT = 9000


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
                receiver = Receiver(conn)
                sender = Sender(conn)
                
                # Odbierz wiadomość Greeting
                greeting = receiver.receive(messages.Greeting)
                print('Received:', greeting.__dict__)
                
                # Wyślij odpowiedź Response
                resp = messages.Response(status=0, message=f"Hello id={greeting.id}")
                sender.send(resp)
                print('Sent response')
            except ConnectionError as e:
                print('Connection closed:', e)

if __name__ == '__main__':
    main()
