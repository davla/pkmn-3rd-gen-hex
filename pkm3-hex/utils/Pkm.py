import itertools
import operator
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Iterable, Literal, Self

from .. import data
from ..data.items import Item
from ..data.locations import Location
from ..data.moves import Move
from ..data.pkm_species import PkmSpecies
from .bytes_handling import read_int


class PkmSubstructuresOrder(StrEnum):
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


@dataclass
class PkmGrowth:
    # Parsed
    species: PkmSpecies
    held_item: Item
    experience: int
    friendship: int

    @property
    def pp_ups(self) -> tuple[int, int, int, int]:
        pp = self.pp_ups_byte
        return (pp & 0x03, pp >> 2 & 0x03, pp >> 4 & 0x03, pp >> 6 & 0x03)

    # Bytes
    pp_ups_byte: int
    data: bytes

    SPECIES_OFFSET = 0x0
    HELD_ITEM_OFFSET = 0x2
    EXP_OFFSET = 0x4
    PP_OFFSET = 0x8
    FRIENDSHIP_OFFSET = 0x9

    @classmethod
    def from_bytes(cls, buffer: bytes) -> Self:
        return cls(
            species=data.pkm_species[
                read_int(buffer[cls.SPECIES_OFFSET : cls.HELD_ITEM_OFFSET])
            ],
            held_item=data.items[
                read_int(buffer[cls.HELD_ITEM_OFFSET : cls.EXP_OFFSET])
            ],
            experience=read_int(buffer[cls.EXP_OFFSET : cls.PP_OFFSET]),
            friendship=buffer[cls.FRIENDSHIP_OFFSET],
            data=buffer,
            pp_ups_byte=buffer[cls.PP_OFFSET],
        )


@dataclass
class PkmAttacks:
    # Parsed
    move1: Move
    move2: Move
    move3: Move
    move4: Move
    pp1: int
    pp2: int
    pp3: int
    pp4: int

    # Bytes
    data: bytes

    MOVE1_OFFSET = 0x0
    MOVE2_OFFSET = 0x2
    MOVE3_OFFSET = 0x4
    MOVE4_OFFSET = 0x6
    PP1_OFFSET = 0x8
    PP2_OFFSET = 0x9
    PP3_OFFSET = 0xA
    PP4_OFFSET = 0xB

    @classmethod
    def from_bytes(cls, buffer: bytes) -> Self:
        return cls(
            move1=data.moves[read_int(buffer[cls.MOVE1_OFFSET : cls.MOVE2_OFFSET])],
            move2=data.moves[read_int(buffer[cls.MOVE2_OFFSET : cls.MOVE3_OFFSET])],
            move3=data.moves[read_int(buffer[cls.MOVE3_OFFSET : cls.MOVE4_OFFSET])],
            move4=data.moves[read_int(buffer[cls.MOVE4_OFFSET : cls.PP1_OFFSET])],
            pp1=buffer[cls.PP1_OFFSET],
            pp2=buffer[cls.PP2_OFFSET],
            pp3=buffer[cls.PP3_OFFSET],
            pp4=buffer[cls.PP4_OFFSET],
            data=buffer,
        )


@dataclass
class PkmEvsAndConditions:
    # Parsed
    hp_evs: int
    atk_evs: int
    def_evs: int
    speed_evs: int
    sp_atk_evs: int
    sp_def_evs: int
    coolness: int
    beauty: int
    cuteness: int
    smartness: int
    toughness: int
    feel: int

    # Bytes
    data: bytes

    HP_EVS_OFFSET = 0x0
    ATK_EVS_OFFSET = 0x1
    DEF_EVS_OFFSET = 0x2
    SPEED_EVS_OFFSET = 0x3
    SP_ATK_EVS_OFFSET = 0x4
    SP_DEF_EVS_OFFSET = 0x5
    COOLNESS_OFFSET = 0x6
    BEAUTY_OFFSET = 0x7
    CUTENESS_OFFSET = 0x8
    SMARTNESS_OFFSET = 0x9
    TOUGHNESS_OFFSET = 0xA
    FEEL_OFFSET = 0xB

    @classmethod
    def from_bytes(cls, buffer: bytes) -> Self:
        return cls(
            hp_evs=read_int(buffer[cls.HP_EVS_OFFSET : cls.ATK_EVS_OFFSET]),
            atk_evs=read_int(buffer[cls.ATK_EVS_OFFSET : cls.DEF_EVS_OFFSET]),
            def_evs=read_int(buffer[cls.DEF_EVS_OFFSET : cls.SPEED_EVS_OFFSET]),
            speed_evs=read_int(buffer[cls.SPEED_EVS_OFFSET : cls.SP_ATK_EVS_OFFSET]),
            sp_atk_evs=read_int(buffer[cls.SP_ATK_EVS_OFFSET : cls.SP_DEF_EVS_OFFSET]),
            sp_def_evs=read_int(buffer[cls.SP_DEF_EVS_OFFSET : cls.COOLNESS_OFFSET]),
            coolness=read_int(buffer[cls.COOLNESS_OFFSET : cls.BEAUTY_OFFSET]),
            beauty=read_int(buffer[cls.BEAUTY_OFFSET : cls.CUTENESS_OFFSET]),
            cuteness=read_int(buffer[cls.CUTENESS_OFFSET : cls.SMARTNESS_OFFSET]),
            smartness=read_int(buffer[cls.SMARTNESS_OFFSET : cls.TOUGHNESS_OFFSET]),
            toughness=read_int(buffer[cls.TOUGHNESS_OFFSET : cls.FEEL_OFFSET]),
            feel=read_int(buffer[cls.FEEL_OFFSET :]),
            data=buffer,
        )


@dataclass
class PkmMisc:
    # Parsed
    @property
    def prks_days_left(self) -> int:
        return self.pkrs_byte & 0x0F

    @property
    def pkrs_strain(self) -> int:
        return (self.pkrs_byte >> 4) & 0x0F

    met_location: Location

    @property
    def original_trainer_gender(self) -> Literal["M", "F"]:
        match (self.origin >> 15) & 0x00_01:
            case 0x00:
                return "M"
            case 0x01:
                return "F"
            case _:
                assert False, "Single-bit bitwise & can only have two values"

    @property
    def caught_poke_ball(self) -> int:
        return (self.origin >> 11) & 0x00_0F

    @property
    def game_of_origin(self) -> int:
        return (self.origin >> 7) & 0x00_0F

    @property
    def level_met(self) -> int:
        return self.origin & 0x00_7F

    @property
    def hp_ivs(self) -> int:
        return self.ivs_egg_ability & 0x00_00_00_0F

    @property
    def atk_ivs(self) -> int:
        return (self.ivs_egg_ability >> 5) & 0x00_00_00_0F

    @property
    def def_ivs(self) -> int:
        return (self.ivs_egg_ability >> 10) & 0x00_00_00_0F

    @property
    def speed_ivs(self) -> int:
        return (self.ivs_egg_ability >> 15) & 0x00_00_00_0F

    @property
    def sp_atk_ivs(self) -> int:
        return (self.ivs_egg_ability >> 20) & 0x00_00_00_0F

    @property
    def sp_def_ivs(self) -> int:
        return (self.ivs_egg_ability >> 25) & 0x00_00_00_0F

    @property
    def is_egg(self) -> bool:
        return (self.ivs_egg_ability >> 30) & 0x00_00_00_01 == 0x00_00_00_01

    @property
    def ability(self) -> int:
        return (self.ivs_egg_ability >> 31) & 0x00_00_00_01

    # Bytes
    pkrs_byte: int
    origin: int
    ivs_egg_ability: int
    ribbons_obedience: int

    data: bytes

    PKRS_OFFSET = 0x0
    MET_LOCATION_OFFSET = 0x1
    ORIGINS_OFFSET = 0x2
    IVS_EGG_ABILITY_OFFSET = 0x4
    RIBBONS_OBEDIENCE_OFFSET = 0x8

    @classmethod
    def from_bytes(cls, buffer: bytes) -> Self:
        return cls(
            pkrs_byte=buffer[cls.PKRS_OFFSET],
            met_location=data.locations[buffer[cls.MET_LOCATION_OFFSET]],
            origin=read_int(buffer[cls.ORIGINS_OFFSET : cls.IVS_EGG_ABILITY_OFFSET]),
            ivs_egg_ability=read_int(
                buffer[cls.IVS_EGG_ABILITY_OFFSET : cls.RIBBONS_OBEDIENCE_OFFSET]
            ),
            ribbons_obedience=read_int(buffer[cls.RIBBONS_OBEDIENCE_OFFSET :]),
            data=buffer,
        )


@dataclass
class PcPkm:
    # Parsed
    personality_value: int
    original_trainer_id: int
    nickname: bytes
    language: int
    is_bad_egg: bool
    original_trainer_name: bytes
    markings: int
    checksum: int

    # Substructures
    substructure_order: PkmSubstructuresOrder
    substructure_encryption_key: int
    growth: PkmGrowth
    attacks: PkmAttacks
    evs_and_conditions: PkmEvsAndConditions
    misc: PkmMisc

    # Bytes
    data: bytes

    PV_OFFSET = 0x00
    OT_ID_OFFSET = 0x04
    NICKNAME_OFFSET = 0x08
    LANGUAGE_OFFSET = 0x12
    MISC_OFFSET = 0x013
    OT_NAME_OFFSET = 0x14
    MARKINGS_OFFSET = 0x1B
    CHECKSUM_OFFSET = 0x1C

    SIZE = 80

    @classmethod
    def from_bytes(cls, buffer: bytes, *, xor_substructures: bool = True) -> Self:
        buffer = bytearray(buffer)

        substructures = cls._Substructures.from_bytes(buffer, xor=xor_substructures)
        if xor_substructures:
            substructures.write_into(buffer)

        # Verify bad egg
        checksum = read_int(buffer[cls.CHECKSUM_OFFSET :], 2)
        if substructures.data_sum() & 0xFF_FF != checksum:
            buffer[cls.MISC_OFFSET] |= 0x01

        return cls(
            personality_value=substructures.pv,
            original_trainer_id=substructures.otid,
            nickname=buffer[cls.NICKNAME_OFFSET : cls.LANGUAGE_OFFSET],
            language=buffer[cls.LANGUAGE_OFFSET],
            is_bad_egg=buffer[cls.MISC_OFFSET] & 0x01 == 0x01,
            original_trainer_name=buffer[cls.OT_NAME_OFFSET : cls.MARKINGS_OFFSET],
            markings=buffer[cls.MARKINGS_OFFSET],
            checksum=checksum,
            substructure_order=substructures.order,
            substructure_encryption_key=substructures.encryption_key,
            growth=PkmGrowth.from_bytes(substructures.get_substructure_bytes("G")),
            attacks=PkmAttacks.from_bytes(substructures.get_substructure_bytes("A")),
            evs_and_conditions=PkmEvsAndConditions.from_bytes(
                substructures.get_substructure_bytes("E")
            ),
            misc=PkmMisc.from_bytes(substructures.get_substructure_bytes("M")),
            data=buffer,
        )

    @classmethod
    def xor_substructures(cls, pkm_bytes: bytearray):
        substructures = cls._Substructures.from_bytes(pkm_bytes, xor=True)
        pkm_bytes[cls._Substructures.OFFSET :] = substructures.data

    @dataclass
    class _Substructures:
        # Computed data
        order: PkmSubstructuresOrder
        encryption_key: int

        # Bytes
        data: bytes

        # Convenience fields
        pv: int
        otid: int

        OFFSET = 0x20
        SINGLE_SUBSTRUCTURE_SIZE = 12
        SIZE = SINGLE_SUBSTRUCTURE_SIZE * 4

        def get_substructure_bytes(
            self,
            substructure: Literal["G", "A", "E", "M"],
        ) -> bytes:
            pos = self.order.value.index(substructure.lower())
            start_index = pos * self.SINGLE_SUBSTRUCTURE_SIZE
            return self.data[start_index : start_index + self.SINGLE_SUBSTRUCTURE_SIZE]

        def write_into(self, pkm_bytes: bytearray):
            pkm_bytes[self.OFFSET :] = self.data

        def data_sum(self) -> int:
            return sum(read_int(bytes(n)) for n in itertools.batched(self.data, 2))

        @classmethod
        def from_bytes(cls, pkm_bytes: bytes, *, xor: bool) -> Self:
            pv_bytes = pkm_bytes[PcPkm.PV_OFFSET : PcPkm.OT_ID_OFFSET]
            otid_bytes = pkm_bytes[PcPkm.OT_ID_OFFSET : PcPkm.NICKNAME_OFFSET]
            encryption_key_bytes = cls._pairwise_xor(pv_bytes, otid_bytes)

            pv = read_int(pv_bytes)
            order = PkmSubstructuresOrder(pv % 24)

            data = pkm_bytes[cls.OFFSET : cls.OFFSET + cls.SIZE]
            if xor:
                data = cls._pairwise_xor(itertools.cycle(encryption_key_bytes), data)

            return cls(
                encryption_key=read_int(encryption_key_bytes),
                order=order,
                data=data,
                pv=pv,
                otid=read_int(otid_bytes),
            )

        @staticmethod
        def _pairwise_xor(b0: Iterable[int], b1: Iterable[int]) -> bytes:
            return bytes(itertools.starmap(operator.xor, zip(b0, b1)))
