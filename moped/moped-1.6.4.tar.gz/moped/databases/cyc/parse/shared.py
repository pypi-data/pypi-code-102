from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from ..data import ParseCompound, ParseReaction

# Often lines starting with these identifiers are malformed
MALFORMED_LINE_STARTS = {
    "/",
    "COMMENT",
    "CITATIONS",
    "^CITATIONS",
    "SYNONYMS",
    "#",
}


def _remove_top_comments(file: List[str]) -> Tuple[List[str], int]:
    """Remove the metainformation from a pgdb file."""
    for i, line in enumerate(file):
        if line.startswith("UNIQUE-ID"):
            break
    return file[i:], i


def _open_file_and_remove_comments(path: Path) -> Tuple[List[str], int]:
    """Read the file and remove metainformation."""
    with open(path, encoding="ISO-8859-14") as f:
        file = f.readlines()
    return _remove_top_comments(file)


def _rename(content: str) -> str:
    """Remove garbage from compound and reaction ids."""
    return (
        content.replace("<i>", "")
        .replace("</i>", "")
        .replace("<SUP>", "")
        .replace("</SUP>", "")
        .replace("<sup>", "")
        .replace("</sup>", "")
        .replace("<sub>", "")
        .replace("</sub>", "")
        .replace("<SUB>", "")
        .replace("</SUB>", "")
        .replace("&", "")
        .replace(";", "")
        .replace("|", "")
    )


def _do_nothing(*args: Any) -> None:
    """Chill. The archetype of a useful function."""
    pass


def _set_gibbs0(dictionary: Dict[str, ParseReaction | ParseCompound], id_: str, gibbs0: str) -> None:
    dictionary[id_].gibbs0 = float(gibbs0)


def _set_name(dictionary: Dict[str, ParseReaction | ParseCompound], id_: str, name: str) -> None:
    dictionary[id_].name = _rename(name)


def _add_database_link(dictionary: Dict[str, ParseReaction | ParseCompound], id_: str, content: str) -> None:
    """Short description.

    Database links are of form DBLINKS - (REFMET "Tryptophan" NIL |midford| 3697479617 NIL NIL)
    so content will be (REFMET "Tryptophan" NIL |midford| 3697479617 NIL NIL)
    """
    database, database_id, *_ = content[1:-1].split(" ")
    dictionary[id_].database_links.setdefault(database, set()).add(database_id[1:-1])


def _add_type(
    dictionary: Dict[str, ParseReaction | ParseCompound],
    id_: str,
    type_: str,
    type_map: Dict[str, str],
) -> None:
    """Short description."""
    dictionary[id_].types.append(type_map.get(type_, type_))
