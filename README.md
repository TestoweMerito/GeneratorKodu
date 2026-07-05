# GeneratorKodu

Projekt pokazuje generator serializacji/deserializacji zdefiniowanej w `interface.json`.

## Instrukcje

1. Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

2. Wygeneruj moduł Pythona zawierający klasy i metody serializacji:

```bash
python generator.py --schema interface.json --templates templates --out generated/messages.py
```

3. Uruchom serwer (w jednym terminalu):

```bash
python server.py
```

4. Uruchom klienta (w drugim terminalu):

```bash
python client.py
```

## Architektura

### `generator.py`
- Czyta plik `interface.json` (definicja struktur danych)
- Używa szablonu Jinja2 (`templates/structs.jinja2`)
- Generuje moduł `generated/messages.py` z klasami i metodami serializacji

### `generated/messages.py`
Wygenerowany moduł zawiera:
- **Funkcje `pack_*` i `unpack_*`** — serializacja/deserializacja typów (int, float, string, bytes, tablice)
- **Klasy `Greeting` i `Response`** — struktury danych z interface.json
- **Metody `to_bytes()` i `from_bytes()`** — konwersja obiektów ↔ bajty

Format binarny: **little-endian**, stringi/bajty prefixowane długością (uint32)

### `generated/transport.py`
Moduł transportu TCP/IP zawiera:
- **`Sender`** — wysyła wiadomości przez gniazdo (metoda `send()`)
- **`Receiver`** — odbiera i deserializuje wiadomości (metoda `receive()`)
- **`MessageHandler`** — kombinacja Sender + Receiver dla wygodniejszej komunikacji

Protokół: `[4-bajtowa-długość-wiadomości][dane-wiadomości]`

### `server.py`
- Nasłuchuje na `127.0.0.1:9000`
- Odbiera wiadomość `Greeting` używając `Receiver`
- Wysyła odpowiedź `Response` używając `Sender`

### `client.py`
- Łączy się z serwerem
- Wysyła `Greeting` używając `Sender`
- Odbiera `Response` używając `Receiver`

## Przykład użycia

**Wysyłanie wiadomości:**
```python
from generated import messages
from generated.transport import Sender

sender = Sender(socket)
greeting = messages.Greeting(
    id=123,
    message='Cześć',
    value=3.14,
    flags=True,
    payload=b'dane',
    numbers=[1, 2, 3]
)
sender.send(greeting)  # Automatycznie serializuje + wysyła
```

**Odbieranie wiadomości:**
```python
from generated.transport import Receiver

receiver = Receiver(socket)
response = receiver.receive(messages.Response)  # Automatycznie odbiera + deserializuje
print(response.message)
```

**Wymiana wiadomości (send + receive):**
```python
from generated.transport import MessageHandler

handler = MessageHandler(socket)
handler.send(greeting)
response = handler.receive(messages.Response)
```

## Pliki

- `interface.json` — definicja struktur danych (JSON schema)
- `templates/structs.jinja2` — szablon Jinja2 do generacji kodu
- `generator.py` — skrypt generatora
- `generated/messages.py` — wygenerowany moduł z klasami i metodami
- `generated/transport.py` — moduł transportu (Sender, Receiver, MessageHandler)
- `server.py` — przykładowy serwer TCP/IP
- `client.py` — przykładowy klient TCP/IP
- `requirements.txt` — zależności
