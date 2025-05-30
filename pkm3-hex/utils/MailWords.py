import itertools
import math
from dataclasses import dataclass
from typing import Iterable, Optional, Self

from ..data import easy_chat
from .Pkm import PcPkm, PkmSubstructuresOrder


@dataclass
class MailWords:
    top_left: Optional[easy_chat.Word]
    top_right: Optional[easy_chat.Word]
    bottom_left: Optional[easy_chat.Word]
    bottom_right: Optional[easy_chat.Word]

    def apply_to_pkm(self, pkm_bytes: bytes, *, is_encrypted: bool = False) -> PcPkm:
        pkm_bytes = (
            pkm_bytes if isinstance(pkm_bytes, bytearray) else bytearray(pkm_bytes)
        )
        if not is_encrypted:
            PcPkm.xor_substructures(pkm_bytes)

        self._set_word(pkm_bytes, self.top_left, at=PcPkm.PV_OFFSET)
        self._set_word(pkm_bytes, self.top_right, at=PcPkm.PV_OFFSET + 2)
        self._set_word(pkm_bytes, self.bottom_left, at=PcPkm.OT_ID_OFFSET)
        self._set_word(pkm_bytes, self.bottom_right, at=PcPkm.OT_ID_OFFSET + 2)

        # Decrypt with new encryption key
        return PcPkm.from_bytes(pkm_bytes, xor_substructures=True)

    def scroll_distance(self) -> int:
        return (
            self._word_scroll_distance(self.top_left)
            + self._word_scroll_distance(self.top_right)
            + self._word_scroll_distance(self.bottom_left)
            + self._word_scroll_distance(self.bottom_right)
        )

    @classmethod
    def find_for_substructure_order(
        cls, pkm: PcPkm, order: PkmSubstructuresOrder
    ) -> Iterable[Self]:
        pv_high, pv_low = cls._split_into_u16(pkm.personality_value)
        tid_high, tid_low = cls._split_into_u16(pkm.original_trainer_id)

        high_word_pairs = cls._find_encryption_word_pairs(pv_high, tid_high)
        low_word_pairs = cls._find_encryption_word_pairs(pv_low, tid_low)
        combinations = itertools.product(high_word_pairs, low_word_pairs)

        for (high_pv, high_tid), (low_pv, low_tid) in combinations:
            pv = high_pv << 16 | low_pv
            if pv % 24 == order.mod24:
                yield MailWords(
                    top_left=easy_chat.words.get(low_pv, None),
                    top_right=easy_chat.words.get(high_pv, None),
                    bottom_left=easy_chat.words.get(low_tid, None),
                    bottom_right=easy_chat.words.get(high_tid, None),
                )

    @staticmethod
    def _find_encryption_word_pairs(b0: int, b1: int) -> Iterable[tuple[int, int]]:
        yield (b0, b1)
        encryption_key = b0 ^ b1
        for word in easy_chat.words.values():
            if word.index == b0:
                continue

            try:
                companion_word = easy_chat.words[word.index ^ encryption_key]
                yield (word.index, companion_word.index)
            except KeyError:
                pass

    @staticmethod
    def _set_word(pkm_bytes: bytearray, word: Optional[easy_chat.Word], *, at: int):
        if word is not None:
            pkm_bytes[at : at + 2] = word.index.to_bytes(length=2, byteorder="little")

    @staticmethod
    def _split_into_u16(n: int) -> tuple[int, int]:
        return (n >> 16 & 0xFF_FF, n & 0xFF_FF)

    @staticmethod
    def _word_scroll_distance(word: Optional[easy_chat.Word]) -> int:
        if word is None:
            return 0

        sorted_words_in_category = list(
            sorted(
                w.text for w in easy_chat.words.values() if w.category == word.category
            )
        )
        return word.category.scroll_distance + math.ceil(
            sorted_words_in_category.index(word.text) / 2
        )


# def verify_mail_words(pkm: PcPkm) -> int:
