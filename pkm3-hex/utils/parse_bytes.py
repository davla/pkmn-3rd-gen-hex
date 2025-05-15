from typing import Literal, Optional


def read_number(buffer: bytes, size: Optional[Literal[2, 4]] = None) -> int:
    b = buffer if size is None else buffer[:size]
    return int.from_bytes(b, byteorder="little")
