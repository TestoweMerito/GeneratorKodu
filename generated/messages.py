"""
Auto-generated serialization helpers and classes template.
"""
import struct
import io

# Primitive pack/unpack helpers
def pack_uint32(v):
    return struct.pack('<I', v)

def unpack_uint32(buf):
    return struct.unpack('<I', buf.read(4))[0]

def pack_int32(v):
    return struct.pack('<i', v)

def unpack_int32(buf):
    return struct.unpack('<i', buf.read(4))[0]

def pack_float(v):
    return struct.pack('<f', v)

def unpack_float(buf):
    return struct.unpack('<f', buf.read(4))[0]

def pack_bool(v):
    return struct.pack('<?', bool(v))

def unpack_bool(buf):
    return struct.unpack('<?', buf.read(1))[0]

def pack_string(s):
    b = (s or '').encode('utf-8')
    return pack_uint32(len(b)) + b

def unpack_string(buf):
    l = unpack_uint32(buf)
    return buf.read(l).decode('utf-8')

def pack_bytes(b):
    b = b or b''
    return pack_uint32(len(b)) + b

def unpack_bytes(buf):
    l = unpack_uint32(buf)
    return buf.read(l)

def pack_array(elem_type, items):
    items = items or []
    out = pack_uint32(len(items))
    for i in items:
        out += globals()['pack_' + elem_type](i)
    return out

def unpack_array(elem_type, buf):
    l = unpack_uint32(buf)
    out = []
    for _ in range(l):
        out.append(globals()['unpack_' + elem_type](buf))
    return out

class Greeting:
    def __init__(self, id=None, message=None, value=None, flags=None, payload=None, numbers=None):
        self.id = id
        self.message = message
        self.value = value
        self.flags = flags
        self.payload = payload
        self.numbers = numbers

    def to_bytes(self):
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
    def __init__(self, status=None, message=None):
        self.status = status
        self.message = message

    def to_bytes(self):
        out = b''
        out += globals()['pack_' + 'uint32'](self.status)
        out += pack_string(self.message)
        return out

    @staticmethod
    def from_bytes(b):
        buf = io.BytesIO(b)
        obj = Response()
        obj.status = globals()['unpack_' + 'uint32'](buf)
        obj.message = unpack_string(buf)
        return obj

