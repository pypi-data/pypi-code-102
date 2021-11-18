from __future__ import annotations

import re
from pathlib import Path
from typing import Dict


class SequenceParser:
    """SequenceParser."""

    def __init__(self, path: Path) -> None:
        with open(path, encoding="ISO-8859-14") as f:
            self.file = f.readlines()

    def parse(self) -> Dict[str, str]:
        """Parse."""
        RE_PAT = re.compile(r"^>gnl\|.*?\|")
        sequences: Dict[str, str] = {}
        for id_, sequence in zip(self.file[::2], self.file[1::2]):
            id_ = re.sub(RE_PAT, "", id_).split(" ", maxsplit=1)[0]
            sequences[id_] = sequence.strip()
        return sequences
