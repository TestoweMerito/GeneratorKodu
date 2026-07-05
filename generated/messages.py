"""
Auto-generated serialization and deserialization module.

Zawiera:
1. Funkcje pack_*/unpack_* — konwertują typy na bajty i odwrotnie
2. Klasy (Greeting, Response) — reprezentują struktury z interface.json
3. Metody to_bytes() i from_bytes() — serializacja/deserializacja do/z formatu binarnego

Format binarny: little-endian, stringi/bajty prefixowane uint32
"""
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
    """Odczytaj 4 bajty (little-endian) ze strumienia i zwróć int32."""
    return struct.unpack('<i', buf.read(4))[0]

def pack_uint64(v):
    """Konwertuj uint64 na 8 bajtów (little-endian)."""
    return struct.pack('<Q', v)

def unpack_uint64(buf):
    """Odczytaj 8 bajtów (little-endian) ze strumienia i zwróć uint64."""
    return struct.unpack('<Q', buf.read(8))[0]

def pack_int64(v):
    """Konwertuj int64 na 8 bajtów (little-endian)."""
    return struct.pack('<q', v)

def unpack_int64(buf):
    """Odczytaj 8 bajtów (little-endian) ze strumienia i zwróć int64."""
    return struct.unpack('<q', buf.read(8))[0]

def pack_float(v):
    """Konwertuj float na 4 bajty (little-endian)."""
    return struct.pack('<f', v)

def unpack_float(buf):
    """Odczytaj 4 bajty (little-endian) ze strumienia i zwróć float."""
    return struct.unpack('<f', buf.read(4))[0]

def pack_double(v):
    """Konwertuj double na 8 bajtów (little-endian)."""
    return struct.pack('<d', v)

def unpack_double(buf):
    """Odczytaj 8 bajtów (little-endian) ze strumienia i zwróć double."""
    return struct.unpack('<d', buf.read(8))[0]

def pack_bool(v):
    """Konwertuj bool na 1 bajt."""
    return struct.pack('<?', bool(v))

def unpack_bool(buf):
    """Odczytaj 1 bajt ze strumienia i zwróć bool."""
    return struct.unpack('<?', buf.read(1))[0]

def pack_string(s):
    """Konwertuj string: [4-bajtowa długość][dane utf-8]."""
    b = (s or '').encode('utf-8')
    return pack_uint32(len(b)) + b

def unpack_string(buf):
    """Odczytaj string: przeczytaj długość, potem dane utf-8."""
    l = unpack_uint32(buf)
    return buf.read(l).decode('utf-8')

def pack_bytes(b):
    """Konwertuj bytes: [4-bajtowa długość][surowe dane]."""
    b = b or b''
    return pack_uint32(len(b)) + b

def unpack_bytes(buf):
    """Odczytaj bytes: przeczytaj długość, potem surowe dane."""
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
    """Struktura 'Greeting' z interface.json.
    
    Pola:
        id (uint32): (pole 1)
        message (string): (pole 2)
        value (float): (pole 3)
        flags (bool): (pole 4)
        payload (bytes): (pole 5)
        numbers (int32[]): (pole 6)
    
    Metody:
        to_bytes(): serializuj obiekt do bajtów
        from_bytes(data): deserializuj obiekt z bajtów
    """
    
    def __init__(self, id=None, message=None, value=None, flags=None, payload=None, numbers=None):
        """Inicjalizuj Greeting.
        
        Args:
            id: uint32
            message: string
            value: float
            flags: bool
            payload: bytes
            numbers: int32[]
        """
        self.id = id
        self.message = message
        self.value = value
        self.flags = flags
        self.payload = payload
        self.numbers = numbers

    def to_bytes(self):
        """Serializuj obiekt do bajtów (format binarny little-endian)."""
        out = b''
        # id: uint32
        out += globals()['pack_' + 'uint32'](self.id)
        # message: string
        out += pack_string(self.message)
        # value: float
        out += globals()['pack_' + 'float'](self.value)
        # flags: bool
        out += globals()['pack_' + 'bool'](self.flags)
        # payload: bytes
        out += pack_bytes(self.payload)
        # numbers: int32[]
        out += pack_array('int32', self.numbers)
        return out

    @staticmethod
    def from_bytes(b):
        """Deserializuj obiekt z bajtów.
        
        Args:
            b: bajty do deserializacji
            
        Returns:
            Greeting: odrestaurowany obiekt
        """
        buf = io.BytesIO(b)
        obj = Greeting()
        # id: uint32
        obj.id = globals()['unpack_' + 'uint32'](buf)
        # message: string
        obj.message = unpack_string(buf)
        # value: float
        obj.value = globals()['unpack_' + 'float'](buf)
        # flags: bool
        obj.flags = globals()['unpack_' + 'bool'](buf)
        # payload: bytes
        obj.payload = unpack_bytes(buf)
        # numbers: int32[]
        obj.numbers = unpack_array('int32', buf)
        return obj
    
    def __repr__(self):
        """Zwróć string reprezentację obiektu."""
        fields = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'Greeting({fields})'

class Response:
    """Struktura 'Response' z interface.json.
    
    Pola:
        status (uint32): (pole 1)
        message (string): (pole 2)
    
    Metody:
        to_bytes(): serializuj obiekt do bajtów
        from_bytes(data): deserializuj obiekt z bajtów
    """
    
    def __init__(self, status=None, message=None):
        """Inicjalizuj Response.
        
        Args:
            status: uint32
            message: string
        """
        self.status = status
        self.message = message

    def to_bytes(self):
        """Serializuj obiekt do bajtów (format binarny little-endian)."""
        out = b''
        # status: uint32
        out += globals()['pack_' + 'uint32'](self.status)
        # message: string
        out += pack_string(self.message)
        return out

    @staticmethod
    def from_bytes(b):
        """Deserializuj obiekt z bajtów.
        
        Args:
            b: bajty do deserializacji
            
        Returns:
            Response: odrestaurowany obiekt
        """
        buf = io.BytesIO(b)
        obj = Response()
        # status: uint32
        obj.status = globals()['unpack_' + 'uint32'](buf)
        # message: string
        obj.message = unpack_string(buf)
        return obj
    
    def __repr__(self):
        """Zwróć string reprezentację obiektu."""
        fields = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'Response({fields})'

