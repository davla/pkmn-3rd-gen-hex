import itertools
from dataclasses import dataclass
from enum import Enum
from typing import Literal, Self

from .bytes_handling import read_int
from .Pkm import PcPkm


@dataclass
class Section:
    class Type(Enum):
        TRAINER_INFO = (0, 3884)
        TEAM_ITEMS = (1, 3968)
        GAME_STATE = (2, 3968)
        MISC = (3, 3968)
        RIVAL = (4, 3848)
        PC_A = (5, 3968)
        PC_B = (6, 3968)
        PC_C = (7, 3968)
        PC_D = (8, 3968)
        PC_E = (9, 3968)
        PC_F = (10, 3968)
        PC_G = (11, 3968)
        PC_H = (12, 3968)
        PC_I = (13, 2000)

        size: int

        def __new__(cls, id: int, size: int):
            self = object.__new__(cls)
            self._value_ = id
            self.size = size
            return self

    data: bytes
    type: Type
    checksum: int
    signature: int
    save_index: int

    DATA_OFFSET = 0x0000
    ID_OFFSET = 0x0FF4
    CHECKSUM_OFFSET = 0x0FF6
    SIGNATURE_OFFSET = 0x0FF8
    SAVE_INDEX_OFFSET = 0x0FFC
    SAVE_INDEX_SIZE = 4

    @property
    def is_pc_start(self) -> bool:
        return self.type == self.Type.PC_A

    @classmethod
    def from_bytes(cls, buffer: bytes) -> Self:
        type = cls.Type(read_int(buffer[cls.ID_OFFSET : cls.CHECKSUM_OFFSET]))
        return cls(
            data=buffer[cls.DATA_OFFSET : type.size],
            type=type,
            checksum=read_int(buffer[cls.CHECKSUM_OFFSET : cls.SIGNATURE_OFFSET]),
            signature=read_int(buffer[cls.SIGNATURE_OFFSET : cls.SAVE_INDEX_OFFSET]),
            save_index=read_int(buffer[cls.SAVE_INDEX_OFFSET :]),
        )


@dataclass
class Pc:
    class Box:
        _pkm: bytes

        ROWS = 5
        COLS = 6
        SIZE = PcPkm.SIZE * ROWS * COLS

        def __init__(self, buffer: bytes):
            self._pkm = buffer

        def __getitem__(self, pos: tuple[int, int]) -> PcPkm:
            row, col = pos
            return PcPkm.from_bytes(
                self.raw_pkm_bytes(row, col), xor_substructures=True
            )

        def raw_pkm_bytes(self, row: int, col: int) -> bytes:
            start = row * self.COLS + col * PcPkm.SIZE
            return self._pkm[start : start + PcPkm.SIZE]

    current_box: int
    boxes: list[Box]
    box_names: list[bytes]
    wallpapers: bytes

    CURRENT_BOX_OFFSET = 0x0000
    PKMN_OFFSET = 0x0004
    BOX_NAMES_OFFSET = 0x8344
    WALLPAPERS_OFFSET = 0x83C2

    BOX_NAME_SIZE = 9

    @classmethod
    def from_bytes(cls, buffer: bytes) -> Self:
        return cls(
            current_box=read_int(buffer[cls.CURRENT_BOX_OFFSET : cls.PKMN_OFFSET]),
            boxes=[
                cls.Box(bytes(b))
                for b in itertools.batched(
                    buffer[cls.PKMN_OFFSET : cls.BOX_NAMES_OFFSET], cls.Box.SIZE
                )
            ],
            box_names=[
                bytes(name)
                for name in itertools.batched(
                    buffer[cls.BOX_NAMES_OFFSET : cls.WALLPAPERS_OFFSET],
                    cls.BOX_NAME_SIZE,
                )
            ],
            wallpapers=buffer[cls.WALLPAPERS_OFFSET :],
        )


@dataclass
class GameSaveBlock:
    type Slot = Literal["A", "B"]

    slot: Slot
    pc: Pc

    A_BLOCK_OFFSET = 0x000000
    B_BLOCK_OFFSET = 0x00E000
    BLOCK_SIZE = B_BLOCK_OFFSET - A_BLOCK_OFFSET

    SECTION_COUNT = 14
    SECTION_SIZE = 4 * (2**10)

    @classmethod
    def from_bytes(cls, save_file: bytes) -> Self:
        (slot_bytes, slot) = cls._find_slot(save_file)
        sections = [
            Section.from_bytes(bytes(section_bytes))
            for section_bytes in itertools.batched(slot_bytes, cls.SECTION_SIZE)
        ]

        pc_sections = itertools.islice(
            itertools.dropwhile(lambda s: not s.is_pc_start, itertools.cycle(sections)),
            0,
            Section.Type.PC_I.value - Section.Type.PC_A.value + 1,
        )

        pc_bytes = bytes(
            itertools.chain.from_iterable(pc_section.data for pc_section in pc_sections)
        )

        return cls(slot, pc=Pc.from_bytes(pc_bytes))

    @classmethod
    def _find_slot(cls, save_file: bytes) -> tuple[bytes, Slot]:
        save_index_a = cls._save_index(cls.A_BLOCK_OFFSET, save_file)
        save_index_b = cls._save_index(cls.B_BLOCK_OFFSET, save_file)
        start, slot = (
            (cls.A_BLOCK_OFFSET, "A")
            if save_index_a > save_index_b
            else (cls.B_BLOCK_OFFSET, "B")
        )
        return save_file[start : start + cls.BLOCK_SIZE], slot

    @classmethod
    def _save_index(cls, block_start: int, save_file: bytes) -> int:
        last_section_offset = cls.SECTION_SIZE * (cls.SECTION_COUNT - 1)
        start = block_start + last_section_offset + Section.SAVE_INDEX_OFFSET
        save_index_bytes = save_file[start : start + Section.SAVE_INDEX_SIZE]
        return read_int(save_index_bytes)
