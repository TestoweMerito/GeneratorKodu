import socket
from generated import messages
from generated.transport import Sender, Receiver

HOST = '127.0.0.1'
PORT = 9000


def main():
    with socket.create_connection((HOST, PORT)) as s:
        sender = Sender(s)
        receiver = Receiver(s)
        
        # Utwórz i wyślij Greeting
        greeting = messages.Greeting(
            id=123,
            message='Cześć serwerze',
            value=3.14,
            flags=True,
            payload=b'bin payload',
            numbers=[1, 2, 3, 4]
        )
        sender.send(greeting)
        print('Sent greeting')
        
        # Odbierz odpowiedź Response
        resp = receiver.receive(messages.Response)
        print('Server replied:', resp.__dict__)

if __name__ == '__main__':
    main()
