import itertools
import math
from dataclasses import dataclass
from typing import Iterator, Self

from ..data import easy_chat
from .Pkm import PcPkm, PkmSubstructuresOrder


@dataclass
class MailWords:
    top_left: easy_chat.Word | int
    top_right: easy_chat.Word | int
    bottom_left: easy_chat.Word | int
    bottom_right: easy_chat.Word | int

    substructures_order: PkmSubstructuresOrder

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
    def from_indices(
        cls, *, top_left: int, top_right: int, bottom_left: int, bottom_right: int
    ) -> Self:
        personality_value = top_right << 16 | top_left
        return cls(
            top_left=easy_chat.words.get(top_left, top_left),
            top_right=easy_chat.words.get(top_right, top_right),
            bottom_left=easy_chat.words.get(bottom_left, bottom_left),
            bottom_right=easy_chat.words.get(bottom_right, bottom_right),
            substructures_order=PkmSubstructuresOrder(personality_value % 24),
        )

    @classmethod
    def find_for_substructure_order(
        cls, pkm: PcPkm, order: PkmSubstructuresOrder
    ) -> Iterator[Self]:
        return (
            words
            for words in cls._words_with_same_encryption_key(pkm)
            if words.substructures_order.name == order.name
        )

    @classmethod
    def find_for_pkm(cls, pkm: PcPkm) -> Iterator[Self]:
        mail_words = sorted(
            cls._words_with_same_encryption_key(pkm),
            key=cls._order_sort_key,
        )
        return (
            next(words)
            for _, words in itertools.groupby(mail_words, key=cls._order_sort_key)
        )

    def _order_sort_key(self) -> str:
        return self.substructures_order.name

    @classmethod
    def _words_with_same_encryption_key(cls, pkm: PcPkm) -> Iterator[Self]:
        pkm_pv_high, pkm_pv_low = cls._split_into_u16(pkm.personality_value)
        pkm_tid_high, pkm_tid_low = cls._split_into_u16(pkm.original_trainer_id)

        high_word_pairs = cls._replacement_words(pkm_pv_high, pkm_tid_high)
        low_word_pairs = cls._replacement_words(pkm_pv_low, pkm_tid_low)
        combinations = itertools.product(high_word_pairs, low_word_pairs)

        return (
            cls.from_indices(
                top_left=low_pv,
                top_right=high_pv,
                bottom_left=low_tid,
                bottom_right=high_tid,
            )
            for (high_pv, high_tid), (low_pv, low_tid) in combinations
            if (high_pv, high_tid, low_pv, low_tid)
            != (pkm_pv_high, pkm_tid_high, pkm_pv_low, pkm_tid_low)
        )

    @staticmethod
    def _replacement_words(i0: int, i1: int) -> Iterator[tuple[int, int]]:
        yield (i0, i1)
        xor = i0 ^ i1
        for word in easy_chat.words.values():
            try:
                companion_word = easy_chat.words[word.index ^ xor]
                yield (word.index, companion_word.index)
            except KeyError:
                pass

    @staticmethod
    def _set_word(pkm_bytes: bytearray, word: easy_chat.Word | int, *, at: int):
        if isinstance(word, easy_chat.Word):
            pkm_bytes[at : at + 2] = word.index.to_bytes(length=2, byteorder="little")

    @staticmethod
    def _split_into_u16(n: int) -> tuple[int, int]:
        return (n >> 16 & 0xFF_FF, n & 0xFF_FF)

    @staticmethod
    def _word_scroll_distance(word: easy_chat.Word | int) -> int:
        if not isinstance(word, easy_chat.Word):
            return 0

        sorted_words_in_category = list(
            sorted(
                w.text for w in easy_chat.words.values() if w.category == word.category
            )
        )
        return word.category.scroll_distance + math.ceil(
            sorted_words_in_category.index(word.text) / 2
        )
