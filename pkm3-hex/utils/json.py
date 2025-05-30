import inspect
from json import JSONDecoder, JSONEncoder
from typing import Any, Callable

from ..data import easy_chat
from .MailWords import MailWords

type KwArgs = dict[str, Any]

type JSONObject = dict[str, Any]
type JSONObjectHook = Callable[[JSONObject], Any]


class PkmJSONSerializer(JSONDecoder, JSONEncoder):
    def __init__(self, *args: Any, **kwargs: Any):
        super(PkmJSONSerializer, self).__init__(
            object_hook=self._object_hook, **constructor_kwargs(JSONDecoder, kwargs)
        )
        super(JSONDecoder, self).__init__(**constructor_kwargs(JSONEncoder, kwargs))

    def default(self, o: Any) -> Any:
        if o is None:
            return None

        if isinstance(o, easy_chat.Word):
            return {"text": o.text, "category": o.category.name}

        if isinstance(o, MailWords):
            return {
                "top_left": self.default(o.top_left),
                "top_right": self.default(o.top_right),
                "bottom_left": self.default(o.bottom_left),
                "bottom_right": self.default(o.bottom_right),
            }
        return o

    @classmethod
    def _object_hook(cls, o: JSONObject) -> Any:
        return cls._try_until_no_key_error(
            o, cls._parse_easy_chat_Word, cls._parse_mail_words
        )

    @staticmethod
    def _parse_easy_chat_Word(o: JSONObject) -> easy_chat.Word | JSONObject:
        try:
            text = o["text"].lower()
            category = easy_chat.Word.Category[o["category"].upper()]
            return next(
                word
                for word in easy_chat.words.values()
                if category == category and text == word.text.lower()
            )
        except StopIteration:
            return o

    @classmethod
    def _parse_mail_words(cls, o: JSONObject) -> MailWords:
        return MailWords.from_indices(
            top_left=o["top_left"],
            top_right=o["top_right"],
            bottom_left=o["bottom_left"],
            bottom_right=o["bottom_right"],
        )

    @staticmethod
    def _try_until_no_key_error(o: JSONObject, *object_hooks: JSONObjectHook) -> Any:
        for hook in object_hooks:
            try:
                return hook(o)
            except KeyError:
                pass
        else:
            return o


def constructor_kwargs(type: type, kwargs: KwArgs) -> KwArgs:
    arg_names = inspect.signature(type.__init__).parameters.keys()
    return {k: v for k, v in kwargs.items() if k in arg_names}
