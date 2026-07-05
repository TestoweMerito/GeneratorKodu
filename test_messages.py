"""
Testy jednostkowe dla wygenerowanego modułu serializacji (generated/messages.py).

Testy sprawdzają:
1. Serializację i deserializację każdego typu
2. Okrągłą konwersję (to_bytes → from_bytes)
3. Zmienne rozmiary danych (stringi, bajty, tablice)
4. Granica wartości dla każdego typu
"""

import unittest
import io
from generated import messages


class TestSerializationTypes(unittest.TestCase):
    """Testy serializacji poszczególnych typów."""
    
    def test_pack_unpack_uint32(self):
        """Test uint32."""
        packed = messages.pack_uint32(42)
        self.assertEqual(len(packed), 4)
        buf = io.BytesIO(packed)
        self.assertEqual(messages.unpack_uint32(buf), 42)
    
    def test_pack_unpack_int32(self):
        """Test int32 (liczby ujemne)."""
        packed = messages.pack_int32(-100)
        buf = io.BytesIO(packed)
        self.assertEqual(messages.unpack_int32(buf), -100)
    
    def test_pack_unpack_uint64(self):
        """Test uint64 (duże liczby)."""
        packed = messages.pack_uint64(9999999999)
        buf = io.BytesIO(packed)
        self.assertEqual(messages.unpack_uint64(buf), 9999999999)
    
    def test_pack_unpack_int64(self):
        """Test int64."""
        packed = messages.pack_int64(-9999999999)
        buf = io.BytesIO(packed)
        self.assertEqual(messages.unpack_int64(buf), -9999999999)
    
    def test_pack_unpack_float(self):
        """Test float."""
        packed = messages.pack_float(3.14)
        buf = io.BytesIO(packed)
        result = messages.unpack_float(buf)
        self.assertAlmostEqual(result, 3.14, places=5)
    
    def test_pack_unpack_double(self):
        """Test double (większa precyzja)."""
        packed = messages.pack_double(3.141592653589793)
        buf = io.BytesIO(packed)
        result = messages.unpack_double(buf)
        self.assertAlmostEqual(result, 3.141592653589793, places=10)
    
    def test_pack_unpack_bool_true(self):
        """Test bool(True)."""
        packed = messages.pack_bool(True)
        buf = io.BytesIO(packed)
        self.assertEqual(messages.unpack_bool(buf), True)
    
    def test_pack_unpack_bool_false(self):
        """Test bool(False)."""
        packed = messages.pack_bool(False)
        buf = io.BytesIO(packed)
        self.assertEqual(messages.unpack_bool(buf), False)
    
    def test_pack_unpack_string(self):
        """Test string (UTF-8)."""
        test_str = "Cześć świecie 你好"
        packed = messages.pack_string(test_str)
        buf = io.BytesIO(packed)
        result = messages.unpack_string(buf)
        self.assertEqual(result, test_str)
    
    def test_pack_unpack_string_empty(self):
        """Test empty string."""
        packed = messages.pack_string("")
        buf = io.BytesIO(packed)
        result = messages.unpack_string(buf)
        self.assertEqual(result, "")
    
    def test_pack_unpack_string_none(self):
        """Test None → empty string."""
        packed = messages.pack_string(None)
        buf = io.BytesIO(packed)
        result = messages.unpack_string(buf)
        self.assertEqual(result, "")
    
    def test_pack_unpack_bytes(self):
        """Test bytes."""
        test_bytes = b'\x00\x01\x02\xff\xfe\xfd'
        packed = messages.pack_bytes(test_bytes)
        buf = io.BytesIO(packed)
        result = messages.unpack_bytes(buf)
        self.assertEqual(result, test_bytes)
    
    def test_pack_unpack_array_int32(self):
        """Test tablica int32."""
        test_array = [1, -100, 0, 999]
        packed = messages.pack_array('int32', test_array)
        buf = io.BytesIO(packed)
        result = messages.unpack_array('int32', buf)
        self.assertEqual(result, test_array)
    
    def test_pack_unpack_array_empty(self):
        """Test pusta tablica."""
        packed = messages.pack_array('int32', [])
        buf = io.BytesIO(packed)
        result = messages.unpack_array('int32', buf)
        self.assertEqual(result, [])


class TestGreetingClass(unittest.TestCase):
    """Testy klasy Greeting (serializacja obiektu)."""
    
    def test_greeting_roundtrip(self):
        """Test: Greeting → to_bytes → from_bytes → Greeting."""
        greeting = messages.Greeting(
            id=123,
            message='Test message',
            value=2.71,
            flags=True,
            payload=b'\x01\x02\x03',
            numbers=[1, 2, 3, 4, 5]
        )
        
        # Serializuj
        packed = greeting.to_bytes()
        self.assertIsInstance(packed, bytes)
        self.assertGreater(len(packed), 0)
        
        # Deserializuj
        unpacked = messages.Greeting.from_bytes(packed)
        
        # Sprawdź pola
        self.assertEqual(unpacked.id, greeting.id)
        self.assertEqual(unpacked.message, greeting.message)
        self.assertAlmostEqual(unpacked.value, greeting.value, places=5)
        self.assertEqual(unpacked.flags, greeting.flags)
        self.assertEqual(unpacked.payload, greeting.payload)
        self.assertEqual(unpacked.numbers, greeting.numbers)
    
    def test_greeting_with_default_values(self):
        """Test Greeting z wartościami domyślnymi (0, '', etc.)."""
        greeting = messages.Greeting(
            id=0,
            message='',
            value=0.0,
            flags=False,
            payload=b'',
            numbers=[]
        )
        packed = greeting.to_bytes()
        unpacked = messages.Greeting.from_bytes(packed)
        
        self.assertEqual(unpacked.id, 0)
        self.assertEqual(unpacked.message, '')
        self.assertEqual(unpacked.value, 0.0)
        self.assertEqual(unpacked.flags, False)
        self.assertEqual(unpacked.payload, b'')
        self.assertEqual(unpacked.numbers, [])
    
    def test_greeting_repr(self):
        """Test __repr__ dla Greeting."""
        greeting = messages.Greeting(id=1, message='test')
        repr_str = repr(greeting)
        self.assertIn('Greeting', repr_str)
        self.assertIn('id=1', repr_str)


class TestResponseClass(unittest.TestCase):
    """Testy klasy Response."""
    
    def test_response_roundtrip(self):
        """Test: Response → to_bytes → from_bytes → Response."""
        response = messages.Response(
            status=200,
            message='OK'
        )
        
        packed = response.to_bytes()
        unpacked = messages.Response.from_bytes(packed)
        
        self.assertEqual(unpacked.status, response.status)
        self.assertEqual(unpacked.message, response.message)
    
    def test_response_repr(self):
        """Test __repr__ dla Response."""
        response = messages.Response(status=200, message='OK')
        repr_str = repr(response)
        self.assertIn('Response', repr_str)
        self.assertIn('status=200', repr_str)


class TestEdgeCases(unittest.TestCase):
    """Testy przypadków granicznych i błędów."""
    
    def test_greeting_large_string(self):
        """Test duży string w Greeting."""
        large_msg = "x" * 10000
        greeting = messages.Greeting(
            id=1,
            message=large_msg,
            value=0,
            flags=False,
            payload=b'',
            numbers=[]
        )
        packed = greeting.to_bytes()
        unpacked = messages.Greeting.from_bytes(packed)
        self.assertEqual(unpacked.message, large_msg)
    
    def test_greeting_large_array(self):
        """Test duża tablica w Greeting."""
        large_array = list(range(10000))
        greeting = messages.Greeting(
            id=1,
            message='',
            value=0,
            flags=False,
            payload=b'',
            numbers=large_array
        )
        packed = greeting.to_bytes()
        unpacked = messages.Greeting.from_bytes(packed)
        self.assertEqual(unpacked.numbers, large_array)
    
    def test_greeting_special_chars_in_string(self):
        """Test znaki specjalne w stringach."""
        special_msg = "Nowy wiersz:\nTab:\tCytowanie:\" i cudzysłów: '"
        greeting = messages.Greeting(
            id=1,
            message=special_msg,
            value=0,
            flags=False,
            payload=b'',
            numbers=[]
        )
        packed = greeting.to_bytes()
        unpacked = messages.Greeting.from_bytes(packed)
        self.assertEqual(unpacked.message, special_msg)


class TestBinaryFormat(unittest.TestCase):
    """Testy formatu binarnego (little-endian, nagłówki, itd.)."""
    
    def test_uint32_little_endian(self):
        """Test little-endian dla uint32 (0x12345678 = [78, 56, 34, 12])."""
        packed = messages.pack_uint32(0x12345678)
        expected = b'\x78\x56\x34\x12'
        self.assertEqual(packed, expected)
    
    def test_string_header_length(self):
        """Test prefiks długości w stringach."""
        packed = messages.pack_string("ABC")  # 3 znaki = 3 bajty
        # Powinno być: [3, 0, 0, 0 (little-endian)] + "ABC"
        self.assertEqual(len(packed), 4 + 3)
        self.assertEqual(packed[4:], b'ABC')
    
    def test_array_header_length(self):
        """Test prefiks liczby elementów w tablicach."""
        packed = messages.pack_array('uint32', [1, 2, 3])
        # Powinno być: [3, 0, 0, 0] + [dane]
        buf = io.BytesIO(packed)
        count = messages.unpack_uint32(buf)
        self.assertEqual(count, 3)


if __name__ == '__main__':
    unittest.main()
