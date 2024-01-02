import inspect
from dataclasses import *

from utils import *


@dataclass
class BlockBase:
    object: str
    id: str


# @dataclass
class Annotations:
    # bold: bool = False
    # italic: bool = False
    # strikethrough: bool = False
    # underline: bool = False
    # code: bool = False
    # color: str = "default"
    def __init__(self, *args):
        for k in args:
            member_name = k
            print(member_name)
            # self.f"{k}" = True


@dataclass
class RichText:
    plain_text: str
    type: str = "text"
    href: str = None
    annotations: list = None
    text: dict = None

    def __post_init__(self):
        self.text = dict(content=self.plain_text, link=self.href)
        # annos = {s: True for s in self.annotations if hasattr(Annotations, s)}


# ano = Annotations()
# text = Text("nihao")
# block = RichText("nihao", annotations=["bold", "italic"])
# print(hasattr(Annotations, "bold"))

anno = Annotations(["bold", "italic"])
# print(anno.__dict__)
