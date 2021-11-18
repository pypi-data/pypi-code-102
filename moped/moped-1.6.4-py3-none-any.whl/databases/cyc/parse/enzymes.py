from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Callable, Dict

from ..data import ParseEnzyme
from .shared import MALFORMED_LINE_STARTS, _do_nothing, _open_file_and_remove_comments

logger = logging.getLogger(__name__)


def _set_enzyme(enzrxns: Dict[str, ParseEnzyme], id_: str, enzyme: str) -> None:
    enzrxns[id_].enzyme = enzyme


def _add_kcat(enzrxns: Dict[str, ParseEnzyme], id_: str, substrate: str, kcat: str) -> None:
    enzrxns[id_].kcat.setdefault(substrate, float(kcat))


def _add_km(enzrxns: Dict[str, ParseEnzyme], id_: str, substrate: str, km: str) -> None:
    enzrxns[id_].km.setdefault(substrate, float(km))


def _add_vmax(enzrxns: Dict[str, ParseEnzyme], id_: str, substrate: str, vmax: str) -> None:
    enzrxns[id_].vmax.setdefault(substrate, float(vmax))


class EnzymeParser:
    """Enzyme Parser."""

    def __init__(self, path: Path) -> None:
        file, start_idx = _open_file_and_remove_comments(path)
        self.file = file
        self.start_idx = start_idx
        self.actions: Dict[str, Callable[[Any, Any, Any], None]] = {
            "UNIQUE-ID": _do_nothing,
            "TYPES": _do_nothing,
            "COMMON-NAME": _do_nothing,
            "ALTERNATIVE-COFACTORS": _do_nothing,
            "ALTERNATIVE-SUBSTRATES": _do_nothing,
            "BASIS-FOR-ASSIGNMENT": _do_nothing,
            "CITATIONS": _do_nothing,
            "COFACTOR-BINDING-COMMENT": _do_nothing,
            "COFACTORS": _do_nothing,
            "COMMENT": _do_nothing,
            "CREDITS": _do_nothing,
            "DATA-SOURCE": _do_nothing,
            "DBLINKS": _do_nothing,
            "DOCUMENTATION": _do_nothing,
            "ENZRXN-IN-PATHWAY": _do_nothing,
            "ENZYME": _set_enzyme,
            "HIDE-SLOT?": _do_nothing,
            "INSTANCE-NAME-TEMPLATE": _do_nothing,
            "KCAT": _do_nothing,
            "KM": _do_nothing,
            "MEMBER-SORT-FN": _do_nothing,
            "PATHOLOGIC-NAME-MATCHER-EVIDENCE": _do_nothing,
            "PATHOLOGIC-PWY-EVIDENCE": _do_nothing,
            "PH-OPT": _do_nothing,
            "PHYSIOLOGICALLY-RELEVANT?": _do_nothing,
            "REACTION": _do_nothing,
            "REACTION-DIRECTION": _do_nothing,
            "REGULATED-BY": _do_nothing,
            "REQUIRED-PROTEIN-COMPLEX": _do_nothing,
            "SPECIFIC-ACTIVITY": _do_nothing,
            "SYNONYMS": _do_nothing,
            "TEMPERATURE-OPT": _do_nothing,
            "VMAX": _do_nothing,
            "ENZRXN-EC-NUMBER": _do_nothing,
        }
        self.sub_actions: Dict[str, Dict[str, Callable[[Any, Any, Any, Any], None]]] = {
            "^SUBSTRATE": {"KM": _add_km, "VMAX": _add_vmax, "KCAT": _add_kcat},
            "^CITATIONS": {
                "KM": _do_nothing,
                "VMAX": _do_nothing,
                "KCAT": _do_nothing,
            },
        }

    def parse(self) -> Dict[str, ParseEnzyme]:
        """Parse."""
        id_ = ""
        enzrxns = {}
        for line in self.file:
            if any(line.startswith(i) for i in MALFORMED_LINE_STARTS):
                continue
            else:
                identifier, content = line.rstrip().split(" - ", maxsplit=1)
                if identifier == "UNIQUE-ID":
                    id_ = content
                    enzrxns[id_] = ParseEnzyme(id=id_)
                elif not identifier.startswith("^"):
                    try:
                        self.actions[identifier](enzrxns, id_, content)
                        last_identifier = identifier
                        last_content = content
                    except KeyError:
                        logger.info(f"Unknown identifier {identifier} for enzyme {id_}")
                else:
                    self.sub_actions[identifier][last_identifier](enzrxns, id_, content, last_content)
        return enzrxns
