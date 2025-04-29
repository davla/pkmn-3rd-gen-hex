import functools
import itertools
import operator
from dataclasses import dataclass
from typing import Iterable


@dataclass
class PkmSubstructures:
    order: str
    growth: bytes
    attacks: bytes
    evs: bytes
    misc: bytes

    start = 32
    size = 12
    count = 4
    end = start + size * count

    order_dict = {
        0: "GAEM",
        1: "GAME",
        2: "GEAM",
        3: "GEMA",
        4: "GMAE",
        5: "GMEA",
        6: "AGEM",
        7: "AGME",
        8: "AEGM",
        9: "AEMG",
        10: "AMGE",
        11: "AMEG",
        12: "EGAM",
        13: "EGMA",
        14: "EAGM",
        15: "EAMG",
        16: "EMGA",
        17: "EMAG",
        18: "MGAE",
        19: "MGEA",
        20: "MAGE",
        21: "MAEG",
        22: "MEGA",
        23: "MEAG",
    }

    def as_bytes(self) -> bytes:
        return bytes(
            itertools.chain.from_iterable(
                bytes
                for _, bytes in sorted(
                    (
                        (self.order.index("G"), self.growth),
                        (self.order.index("A"), self.attacks),
                        (self.order.index("E"), self.evs),
                        (self.order.index("M"), self.misc),
                    )
                )
            )
        )

    @classmethod
    def from_bytes(cls, bytes: bytes, *, decrypt: bool = True):
        personality_value = int.from_bytes(bytes[0:4], byteorder="little")
        order = cls.order_dict[personality_value % 24]
        return cls(
            order,
            growth=cls._get_substructure_at(bytes, order.index("G"), decrypt),
            attacks=cls._get_substructure_at(bytes, order.index("A"), decrypt),
            evs=cls._get_substructure_at(bytes, order.index("E"), decrypt),
            misc=cls._get_substructure_at(bytes, order.index("M"), decrypt),
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
