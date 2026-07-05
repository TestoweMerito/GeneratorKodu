# GeneratorKodu

Projekt pokazuje generator serializacji/deserializacji zdefiniowanej w `interface.json`.

Instrukcje:

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

Opis:
- `generator.py` — czyta `interface.json` i używa `templates/structs.jinja2` do wygenerowania `generated/messages.py`.
- `server.py` oraz `client.py` — przykład komunikacji TCP wykorzystujący wygenerowane metody `to_bytes()`/`from_bytes()`.
