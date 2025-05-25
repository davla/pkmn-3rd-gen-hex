import itertools
import math
from dataclasses import dataclass
from typing import Iterable, Optional

from ..data import easy_chat
from .bytes_handling import read_int
from .Pkm import PcPkm, PkmSubstructuresOrder


@dataclass
class MailWords:
    top_left: Optional[easy_chat.Word]
    top_right: Optional[easy_chat.Word]
    bottom_left: Optional[easy_chat.Word]
    bottom_right: Optional[easy_chat.Word]

    def scroll_distance(self) -> int:
        return (
            self._word_scroll_distance(self.top_left)
            + self._word_scroll_distance(self.top_right)
            + self._word_scroll_distance(self.bottom_left)
            + self._word_scroll_distance(self.bottom_right)
        )

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


def apply_mail_words(
    pkm: PcPkm | bytes, words: MailWords, *, is_encrypted: bool = False
) -> PcPkm:
    pkm_bytes = bytearray(pkm.data if isinstance(pkm, PcPkm) else pkm)
    if not is_encrypted:
        PcPkm.xor_substructures(pkm_bytes)

    set_word(pkm_bytes, words.top_left, at=PcPkm.PV_OFFSET)
    set_word(pkm_bytes, words.top_right, at=PcPkm.PV_OFFSET + 2)
    set_word(pkm_bytes, words.bottom_left, at=PcPkm.OT_ID_OFFSET)
    set_word(pkm_bytes, words.bottom_right, at=PcPkm.OT_ID_OFFSET + 2)

    # Decrypt with new encryption key
    return PcPkm.from_bytes(pkm_bytes, xor_substructures=True)


def set_word(pkm_bytes: bytearray, word: Optional[easy_chat.Word], *, at: int):
    if word is not None:
        pkm_bytes[at : at + 2] = word.index.to_bytes(length=2, byteorder="little")


def find_mail_words(
    pkm_bytes: bytes, order: PkmSubstructuresOrder
) -> Iterable[MailWords]:
    pv_high, pv_low = read_int(pkm_bytes[2:], 2), read_int(pkm_bytes, 2)
    tid_high, tid_low = read_int(pkm_bytes[6:], 2), read_int(pkm_bytes[4:], 2)

    high_word_pairs = find_encryption_word_pairs(pv_high, tid_high)
    low_word_pairs = find_encryption_word_pairs(pv_low, tid_low)
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


def find_encryption_word_pairs(b0: int, b1: int) -> Iterable[tuple[int, int]]:
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
