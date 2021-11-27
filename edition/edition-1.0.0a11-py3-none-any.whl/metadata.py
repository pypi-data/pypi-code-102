from typing import Optional, TypedDict

from comprehemd.outline import Outline


class Metadata(TypedDict, total=False):
    body: Optional[str]
    css: Optional[str]
    title: Optional[str]
    toc: Optional[Outline]
