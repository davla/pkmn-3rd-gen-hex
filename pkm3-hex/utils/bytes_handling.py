from typing import Literal, Optional

type NumberByteSize = Literal[1, 2, 4]


def format_hex(
    n: int, *, byte_size: NumberByteSize, separator: str = "_", prefix: bool = True
) -> str:
    buffer = int.to_bytes(n, byte_size, byteorder="big")
    return f"{'0x' if prefix else ''}{format_bytes(buffer, separator=separator)}"


def format_bytes(buffer: bytes, *, separator: str = " ") -> str:
    return separator.join(f"{b:02X}" for b in buffer)


def read_int(buffer: bytes, size: Optional[Literal[2, 4]] = None) -> int:
    b = buffer if size is None else buffer[:size]
    return int.from_bytes(b, byteorder="little")
