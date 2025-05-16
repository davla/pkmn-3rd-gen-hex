import functools
import itertools
import operator
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Iterable, Self

from .bytes_handling import read_int


@dataclass
class PkmSubstructures:
    class Order(StrEnum):
        GAEM = (auto(), 0)
        GAME = (auto(), 1)
        GEAM = (auto(), 2)
        GEMA = (auto(), 3)
        GMAE = (auto(), 4)
        GMEA = (auto(), 5)
        AGEM = (auto(), 6)
        AGME = (auto(), 7)
        AEGM = (auto(), 8)
        AEMG = (auto(), 9)
        AMGE = (auto(), 10)
        AMEG = (auto(), 11)
        EGAM = (auto(), 12)
        EGMA = (auto(), 13)
        EAGM = (auto(), 14)
        EAMG = (auto(), 15)
        EMGA = (auto(), 16)
        EMAG = (auto(), 17)
        MGAE = (auto(), 18)
        MGEA = (auto(), 19)
        MAGE = (auto(), 20)
        MAEG = (auto(), 21)
        MEGA = (auto(), 22)
        MEAG = (auto(), 23)

        mod24: int

        def __new__(cls, name: str, mod24: int) -> Self:
            self = str.__new__(cls)
            self._value_ = name
            self.mod24 = mod24
            self._add_value_alias_(mod24)  # type: ignore
            return self

    order: Order
    growth: bytes
    attacks: bytes
    evs: bytes
    misc: bytes

    start = 32
    size = 12
    count = 4
    end = start + size * count

    def as_bytes(self) -> bytes:
        return bytes(
            itertools.chain.from_iterable(
                bytes
                for _, bytes in sorted(
                    (
                        (self.order.name.index("G"), self.growth),
                        (self.order.name.index("A"), self.attacks),
                        (self.order.name.index("E"), self.evs),
                        (self.order.name.index("M"), self.misc),
                    )
                )
            )
        )

    @classmethod
    def from_bytes(cls, bytes: bytes, *, decrypt: bool = True):
        personality_value = read_int(bytes, 4)
        order = cls.Order(personality_value % 24)
        return cls(
            order,
            growth=cls._get_substructure_at(bytes, order.name.index("G"), decrypt),
            attacks=cls._get_substructure_at(bytes, order.name.index("A"), decrypt),
            evs=cls._get_substructure_at(bytes, order.name.index("E"), decrypt),
            misc=cls._get_substructure_at(bytes, order.name.index("M"), decrypt),
        )

    @classmethod
    def _get_substructure_at(cls, buffer: bytes, index: int, decrypt: bool) -> bytes:
        start_index = cls.start + index * cls.size
        substructure_bytes = buffer[start_index : start_index + cls.size]

        if decrypt:
            personality_value = buffer[0:4]
            ot_id = buffer[4:8]
            byte_triplets = zip(
                itertools.cycle(personality_value),
                itertools.cycle(ot_id),
                substructure_bytes,
            )
            substructure_bytes = bytes(map(cls._multi_xor, byte_triplets))

        return substructure_bytes

    @staticmethod
    def _multi_xor(items: Iterable[int]) -> int:
        return functools.reduce(operator.xor, items)
