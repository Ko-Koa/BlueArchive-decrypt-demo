import base64

from xxhash import xxh32

from .mersenne_twister import MersenneTwister


def XOR(plaintext: bytearray, name: str):
    xxhash = xxh32()
    xxhash.update(name.encode("utf-8"))
    seed = xxhash.intdigest()

    mt = MersenneTwister(seed)
    key = mt.NextBytes(len(plaintext))
    for index in range(len(plaintext)):
        plaintext[index] ^= key[index]

    return plaintext


def zip_password(zip_name: str, length: int = 20) -> str:
    """
    计算压缩包密码

    :param zip_name: 压缩包名称,可输入'xxx.zip'或者'xxx'
    :type zip_name: str
    :param length: 密码长度,默认为20
    :type length: int
    :return: 压缩包密码
    :rtype: str
    """
    if ".zip" not in zip_name:
        zip_name += ".zip"

    key = zip_name.encode("utf-8")
    xxhash = xxh32()
    xxhash.update(key)
    seed = xxhash.intdigest() & 0xFFFFFFFF

    byte_count = (3 * length) // 4
    mt = MersenneTwister(seed)
    password_bytes = mt.NextBytes(byte_count)
    return base64.b64encode(password_bytes).decode("utf-8")


def create_key(name: str, length: int = 20):
    xxhash = xxh32()
    xxhash.update(name.encode("utf-8"))
    seed = xxhash.intdigest()

    mt = MersenneTwister(seed)
    return mt.NextBytes(length)


__all__ = ["zip_password", "create_key", "XOR"]
