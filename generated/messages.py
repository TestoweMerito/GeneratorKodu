import struct
import io

# ============================================================================
# FUNKCJE POMOCNICZE - Pack/Unpack (serializacja/deserializacja typów)
# ============================================================================

def pack_uint32(v):
    """Konwertuj uint32 na 4 bajty (little-endian)."""
    return struct.pack('<I', v)

def unpack_uint32(buf):
    """Odczytaj 4 bajty (little-endian) ze strumienia i zwróć uint32."""
    return struct.unpack('<I', buf.read(4))[0]

def pack_int32(v):
    """Konwertuj int32 na 4 bajty (little-endian)."""
    return struct.pack('<i', v)

def unpack_int32(buf):
    return struct.unpack('<i', buf.read(4))[0]

def pack_float(v):
    """Konwertuj float na 4 bajty (little-endian)."""
    return struct.pack('<f', v)

def unpack_float(buf):
    return struct.unpack('<f', buf.read(4))[0]

def pack_bool(v):
    """Konwertuj bool na 1 bajt."""
    return struct.pack('<?', bool(v))

def unpack_bool(buf):
    return struct.unpack('<?', buf.read(1))[0]

def pack_string(s):
    """Konwertuj string: [4-bajtowa długość][dane utf-8]."""
    b = (s or '').encode('utf-8')
    return pack_uint32(len(b)) + b

def unpack_string(buf):
    l = unpack_uint32(buf)
    return buf.read(l).decode('utf-8')

def pack_bytes(b):
    """Konwertuj bytes: [4-bajtowa długość][surowe dane]."""
    b = b or b''
    return pack_uint32(len(b)) + b

def unpack_bytes(buf):
    l = unpack_uint32(buf)
    return buf.read(l)

def pack_array(elem_type, items):
    """Konwertuj tablicę: [liczba elementów][elementy]."""
    items = items or []
    out = pack_uint32(len(items))
    for i in items:
        out += globals()['pack_' + elem_type](i)
    return out

def unpack_array(elem_type, buf):
    """Odczytaj tablicę: przeczytaj liczbę elementów, potem każdy element."""
    l = unpack_uint32(buf)
    out = []
    for _ in range(l):
        out.append(globals()['unpack_' + elem_type](buf))
    return out

# ============================================================================
# KLASY - Struktury danych (wygenerowane z interface.json)
# ============================================================================

class Greeting:
    """Struktura wiadomości powitania (z interface.json).
    
    Pola:
        id (uint32): identyfikator wiadomości
        message (string): treść powitania
        value (float): wartość numeryczna
        flags (bool): flaga logiczna
        payload (bytes): dane binarne
        numbers (int32[]): tablica liczb całkowitych
    
    Metody:
        to_bytes(): serializuj obiekt do bajtów
        from_bytes(data): deserializuj obiekt z bajtów
    """
    def __init__(self, id=None, message=None, value=None, flags=None, payload=None, numbers=None):
        self.id = id
        self.message = message
        self.value = value
        self.flags = flags
        self.payload = payload
        self.numbers = numbers

    def to_bytes(self):
        """Serializuj obiekt Greeting na bajty (format binarny little-endian)."""
        out = b''
        out += globals()['pack_' + 'uint32'](self.id)
        out += pack_string(self.message)
        out += globals()['pack_' + 'float'](self.value)
        out += globals()['pack_' + 'bool'](self.flags)
        out += pack_bytes(self.payload)
        out += pack_array('int32', self.numbers)
        return out

    @staticmethod
    def from_bytes(b):
        """Deserializuj obiekt Greeting z bajtów.
        
        Args:
            b: bajty do deserializacji
            
        Returns:
            Greeting: odrestaurowany obiekt
        """
        buf = io.BytesIO(b)
        obj = Greeting()
        obj.id = globals()['unpack_' + 'uint32'](buf)
        obj.message = unpack_string(buf)
        obj.value = globals()['unpack_' + 'float'](buf)
        obj.flags = globals()['unpack_' + 'bool'](buf)
        obj.payload = unpack_bytes(buf)
        obj.numbers = unpack_array('int32', buf)
        return obj

class Response:
    """Struktura wiadomości odpowiedzi (z interface.json).
    
    Pola:
        status (uint32): kod statusu odpowiedzi
        message (string): treść odpowiedzi
    
    Metody:
        to_bytes(): serializuj obiekt do bajtów
        from_bytes(data): deserializuj obiekt z bajtów
    """
    def __init__(self, status=None, message=None):
        self.status = status
        self.message = message

    def to_bytes(self):
        """Serializuj obiekt Response na bajty (format binarny little-endian)."""
        out = b''
        out += globals()['pack_' + 'uint32'](self.status)
        out += pack_string(self.message)
        return out

    @staticmethod
    def from_bytes(b):
        """Deserializuj obiekt Response z bajtów.
        
        Args:
            b: bajty do deserializacji
            
        Returns:
            Response: odrestaurowany obiekt
        """
        buf = io.BytesIO(b)
        obj = Response()
        obj.status = globals()['unpack_' + 'uint32'](buf)
        obj.message = unpack_string(buf)
        return obj

