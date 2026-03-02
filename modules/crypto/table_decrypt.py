import struct
import base64
from typing import Any


class CSharpType:
    """C#类型"""

    # C# 类型范围常量
    UINT_MAX = 4294967295
    ULONG_MAX = 18446744073709551615

    @staticmethod
    def _is_uint(value: int):
        return 0 <= value <= CSharpType.UINT_MAX

    @staticmethod
    def _is_ulong(value: int):
        return 0 <= value <= CSharpType.ULONG_MAX


class TableDecrypt(CSharpType):
    @classmethod
    def decrypt_table_value(cls, data: Any, key: bytearray):
        if isinstance(data, bytes):
            return cls._decrypt_string(data, key)
        elif isinstance(data, int):
            # 先判断 int 再判断 long类型
            if cls._is_uint(data):
                return cls._decrypt_uint(data, key)
            elif cls._is_ulong(data):
                return cls._decrypt_ulong(data, key)

    @classmethod
    def _decrypt_string(cls, cipher: bytes, key: bytearray):
        cipher_bytes = bytearray(base64.b64decode(cipher))
        for index in range(len(cipher_bytes)):
            cipher_bytes[index] ^= key[index % len(key)]
        return cipher_bytes.decode("utf-16-le")

    @classmethod
    def _decrypt_uint(cls, cipher: int, key: bytearray):
        cipher_bytes = bytearray(struct.pack("<I", cipher))
        for index in range(len(cipher_bytes)):
            cipher_bytes[index] ^= key[index]
        return struct.unpack("<I", cipher_bytes[0:4])[0]

    @classmethod
    def _decrypt_ulong(cls, cipher: int, key: bytearray):
        cipher_bytes = bytearray(struct.pack("<Q", cipher))
        for index in range(len(cipher_bytes)):
            cipher_bytes[index] ^= key[index]
        return struct.unpack("<Q", cipher_bytes[0:8])[0]
