"""
Moduł transportu do wysyłania i odbierania wiadomości przez TCP/IP.

Zawiera:
1. Klasa Sender - wysyła wiadomości serializowane do bajtów
2. Klasa Receiver - odbiera i deserializuje wiadomości z bajtów
3. Funkcje pomocnicze do obsługi protokołu (długość wiadomości)

Protokół: [4-bajtowa-długość-wiadomości][dane-wiadomości]
"""

import struct
import io


class Sender:
    """Nadawca wiadomości przez gniazdo TCP/IP.
    
    Przykład użycia:
        sender = Sender(socket)
        greeting = Greeting(id=1, message="Cześć", ...)
        sender.send(greeting)
    """
    
    def __init__(self, socket):
        """Inicjalizuj nadawcę.
        
        Args:
            socket: gniazdo TCP/IP do wysyłania
        """
        self.socket = socket
    
    def send(self, message):
        """Wyślij wiadomość przez gniazdo.
        
        Proces:
        1. Serializuj wiadomość do bajtów (message.to_bytes())
        2. Oblicz długość bajtów
        3. Wyślij nagłówek [4-bajtowa-długość]
        4. Wyślij dane wiadomości
        
        Args:
            message: obiekt z metodą to_bytes() (np. Greeting, Response)
            
        Raises:
            AttributeError: jeśli wiadomość nie ma metody to_bytes()
        """
        data = message.to_bytes()
        length_header = struct.pack('<I', len(data))
        self.socket.sendall(length_header + data)
    
    def send_raw(self, data):
        """Wyślij surowe bajty z nagłówkiem długości.
        
        Args:
            data: bajty do wysłania
        """
        length_header = struct.pack('<I', len(data))
        self.socket.sendall(length_header + data)


class Receiver:
    """Odbiornik wiadomości z gniazda TCP/IP.
    
    Przykład użycia:
        receiver = Receiver(socket)
        greeting = receiver.receive(Greeting)
    """
    
    def __init__(self, socket):
        """Inicjalizuj odbiornik.
        
        Args:
            socket: gniazdo TCP/IP do odbierania
        """
        self.socket = socket
    
    def receive(self, message_class):
        """Odbierz wiadomość i deserializuj ją.
        
        Proces:
        1. Przeczytaj nagłówek [4-bajtowa-długość]
        2. Przeczytaj dane wiadomości
        3. Deserializuj dane (message_class.from_bytes(data))
        4. Zwróć obiekt wiadomości
        
        Args:
            message_class: klasa wiadomości z metodą from_bytes()
                          (np. Greeting, Response)
            
        Returns:
            Instancja message_class zdeserializowana z bajtów
            
        Raises:
            ConnectionError: jeśli gniazdo zostało zamknięte
            AttributeError: jeśli klasa nie ma metody from_bytes()
        """
        data = self.receive_raw()
        return message_class.from_bytes(data)
    
    def receive_raw(self):
        """Odbierz surowe bajty (bez deserializacji).
        
        Najpierw przeczytaj nagłówek długości, potem dane.
        
        Returns:
            Bajty odebranej wiadomości
            
        Raises:
            ConnectionError: jeśli gniazdo zostało zamknięte
        """
        length_data = self._recv_all(4)
        length, = struct.unpack('<I', length_data)
        data = self._recv_all(length)
        return data
    
    def _recv_all(self, n):
        """Wewnętrzna funkcja: odbierz dokładnie n bajtów.
        
        Czyta z gniazda aż do uzbierania n bajtów lub zamknięcia połączenia.
        
        Args:
            n: liczba bajtów do odebrania
            
        Returns:
            Dokładnie n bajtów
            
        Raises:
            ConnectionError: jeśli gniazdo zostało zamknięte przed odebraniem n bajtów
        """
        data = b''
        while len(data) < n:
            chunk = self.socket.recv(n - len(data))
            if not chunk:
                raise ConnectionError('Gniazdo zostało zamknięte')
            data += chunk
        return data


class MessageHandler:
    """Kombinacja sender + receiver dla wygodniejszej komunikacji.
    
    Przykład użycia:
        handler = MessageHandler(socket)
        handler.send(greeting)
        response = handler.receive(Response)
    """
    
    def __init__(self, socket):
        """Inicjalizuj handler.
        
        Args:
            socket: gniazdo TCP/IP
        """
        self.sender = Sender(socket)
        self.receiver = Receiver(socket)
    
    def send(self, message):
        """Wyślij wiadomość."""
        self.sender.send(message)
    
    def receive(self, message_class):
        """Odbierz wiadomość."""
        return self.receiver.receive(message_class)
    
    def exchange(self, send_msg, receive_class):
        """Wyślij wiadomość i odbierz odpowiedź.
        
        Args:
            send_msg: wiadomość do wysłania
            receive_class: klasa wiadomości do odebrania
            
        Returns:
            Odebrany obiekt wiadomości
        """
        self.send(send_msg)
        return self.receive(receive_class)
