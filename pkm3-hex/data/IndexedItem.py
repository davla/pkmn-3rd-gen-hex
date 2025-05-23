from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class IndexedItem(metaclass=ABCMeta):
    name: str
    index: int

    @property
    @abstractmethod
    def is_glitch(self) -> bool:
        raise NotImplementedError(f"{type(self).name} does not implement is_glitch")
