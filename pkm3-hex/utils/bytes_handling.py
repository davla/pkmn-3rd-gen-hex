from typing import Literal, Optional


def format_hex(n: int, *, width: Literal[1, 2, 4]) -> str:
    return f"{n:0{width}X}"


def read_int(buffer: bytes, size: Optional[Literal[2, 4]] = None) -> int:
    b = buffer if size is None else buffer[:size]
    return int.from_bytes(b, byteorder="little")
