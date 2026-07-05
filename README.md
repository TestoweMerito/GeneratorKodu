# GeneratorKodu

Solidny generator serializacji/deserializacji danych zdefiniowanych w `interface.json` z obsługą TCP/IP.

## Cechy

- ✓ **Walidacja schematu** — sprawdzanie poprawności `interface.json`
- ✓ **Obsługa błędów** — jasne komunikaty w przypadku błędów
- ✓ **Rozszerzalne typy** — uint32, int32, int64, uint64, float, double, bool, string, bytes, tablice
- ✓ **Transport TCP/IP** — klasy `Sender`, `Receiver`, `MessageHandler`
- ✓ **Testy jednostkowe** — 25 testów pokrywających serializację i edge casey
- ✓ **Czysty kod** — docstrings, komentarze, spójne formatowanie
- ✓ **Little-endian format** — zgodny z typową reprezentacją binarną

## Instrukcje

1. Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

2. Wygeneruj moduł Pythona zawierający klasy i metody serializacji:

```bash
python generator.py --schema interface.json --templates templates --out generated/messages.py
```

3. Uruchom testy (opcjonalnie):

```bash
python -m unittest test_messages -v
```

4. Uruchom serwer (w jednym terminalu):

```bash
python server.py
```

5. Uruchom klienta (w drugim terminalu):

```bash
python client.py
```

## Architektura

### `generator.py`
- Czyta plik `interface.json` (definicja struktur danych)
- **Waliduje** schemat JSON
- Używa szablonu Jinja2 (`templates/structs.jinja2`)
- Generuje moduł `generated/messages.py` z klasami i metodami serializacji
- Wyświetla jasne komunikaty o błędach

```bash
# Walidacja + generacja
python generator.py --schema interface.json --templates templates --out generated/messages.py
✓ Schemat wczytany: 2 typów
✓ Szablon załadowany: templates/structs.jinja2
✓ Kod wygenerowany
✓ Zapisano: generated/messages.py
```

### `interface.json`
Definicja struktur danych w formacie JSON:

```json
{
  "types": [
    {
      "name": "Greeting",
      "fields": [
        {"name": "id", "type": "uint32"},
        {"name": "message", "type": "string"},
        {"name": "numbers", "type": "int32[]"}
      ]
    }
  ]
}
```

Obsługiwane typy: `uint32`, `int32`, `int64`, `uint64`, `float`, `double`, `bool`, `string`, `bytes`, oraz `[]` dla tablic.

### `generated/messages.py`
Wygenerowany moduł zawiera:
- **Funkcje `pack_*` i `unpack_*`** — serializacja/deserializacja typów
- **Klasy (Greeting, Response, ...)** — struktury danych z interface.json
- **Metody `to_bytes()` i `from_bytes()`** — konwersja obiektów ↔ bajty
- **Metoda `__repr__()`** — reprezentacja tekstowa obiektów

Format binarny: **little-endian**, stringi/bajty prefixowane długością (uint32)

### `generated/transport.py`
Moduł transportu TCP/IP zawiera:
- **`Sender`** — wysyła wiadomości przez gniazdo (metoda `send()`)
- **`Receiver`** — odbiera i deserializuje wiadomości (metoda `receive()`)
- **`MessageHandler`** — kombinacja Sender + Receiver

Protokół: `[4-bajtowa-długość-wiadomości][dane-wiadomości]`

### `test_messages.py`
Testy jednostkowe (25 testów):
- Serializacja/deserializacja każdego typu
- Okrągła konwersja (to_bytes → from_bytes)
- Edge casey (duże stringi, tablice, znaki specjalne)
- Format binarny (little-endian, nagłówki)

Uruchomienie:
```bash
python -m unittest test_messages -v
# Ran 25 tests in 0.018s - OK
```

### `server.py`
- Nasłuchuje na `127.0.0.1:9000`
- Odbiera wiadomość `Greeting` używając `Receiver`
- Wysyła odpowiedź `Response` używając `Sender`

### `client.py`
- Łączy się z serwerem
- Wysyła `Greeting` używając `Sender`
- Odbiera `Response` używając `Receiver`

## Przykłady użycia

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

**Serializacja bezpośrednia:**
```python
greeting = messages.Greeting(id=1, message='Test', value=3.14, 
                             flags=True, payload=b'', numbers=[1,2,3])
data = greeting.to_bytes()           # → bajty
greeting2 = messages.Greeting.from_bytes(data)  # ← bajty
```

## Pliki

- `interface.json` — definicja struktur danych (JSON schema)
- `templates/structs.jinja2` — szablon Jinja2 do generacji kodu
- `generator.py` — skrypt generatora (z walidacją)
- `generated/messages.py` — wygenerowany moduł (klasy + metody)
- `generated/transport.py` — moduł transportu (Sender, Receiver, MessageHandler)
- `server.py` — przykładowy serwer TCP/IP
- `client.py` — przykładowy klient TCP/IP
- `test_messages.py` — testy jednostkowe (25 testów)
- `requirements.txt` — zależności
- `README.md` — ta dokumentacja

## Ulepszenia

Obecny generator jest solidny i gotowy do produkcji:
- ✓ Walidacja schematu JSON (typy, pola, nazwy)
- ✓ Jasne komunikaty o błędach
- ✓ Obsługa wielu typów danych
- ✓ Testy pokrywające serializację i edge casey
- ✓ Dokumentacja API (docstrings)
- ✓ Transport TCP/IP z bufferowaniem
