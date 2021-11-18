from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict

from ....core.reaction import Monomer
from ..data import ParseGene
from .shared import (
    MALFORMED_LINE_STARTS,
    _add_database_link,
    _do_nothing,
    _open_file_and_remove_comments,
)


def _set_gene_product(genes: Dict[str, ParseGene], id_: str, product: str) -> None:
    genes[id_].product = product


class GeneParser:
    def __init__(self, path: Path) -> None:
        file, start_idx = _open_file_and_remove_comments(path)
        self.file = file
        self.start_idx = start_idx

        self.actions: Dict[str, Callable[[Any, Any, Any], None]] = {
            "DBLINKS": _add_database_link,
            "PRODUCT": _set_gene_product,
        }

    def parse(self) -> Dict[str, Monomer]:
        genes: Dict[str, ParseGene] = {}
        for line in self.file:
            if any(line.startswith(i) for i in MALFORMED_LINE_STARTS):
                continue
            identifier, content = line.rstrip().split(" - ", maxsplit=1)
            if identifier == "UNIQUE-ID":
                id_ = content
                genes[content] = ParseGene(id=content)
            else:
                self.actions.get(identifier, _do_nothing)(genes, id_, content)
        return {
            product: Monomer(id=product, gene=i.id, database_links=i.database_links)
            for i in genes.values()
            if (product := i.product) is not None
        }
