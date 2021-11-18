from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Callable, Dict, Set, Tuple

from .shared import MALFORMED_LINE_STARTS, _do_nothing, _open_file_and_remove_comments

logger = logging.getLogger(__name__)


def _add_component(complexes: Dict[str, Set[str]], complex_id: str, component: str) -> None:
    complexes[complex_id].add(component)


class ProteinParser:
    """Protein parser."""

    def __init__(self, path: Path) -> None:
        file, start_idx = _open_file_and_remove_comments(path)
        self.file = file
        self.start_idx = start_idx
        self.actions: Dict[str, Callable[[Any, Any, Any], None]] = {
            # "UNIQUE-ID": _do_nothing,
            "TYPES": _do_nothing,
            "COMMON-NAME": _do_nothing,
            "ABBREV-NAME": _do_nothing,
            "ACCESSION-1": _do_nothing,
            "AROMATIC-RINGS": _do_nothing,
            "ATOM-CHARGES": _do_nothing,
            "ATOM-ISOTOPES": _do_nothing,
            "CATALYZES": _do_nothing,
            "CHEMICAL-FORMULA": _do_nothing,
            "CITATIONS": _do_nothing,
            "CODING-SEGMENTS": _do_nothing,
            "COFACTORS-OF": _do_nothing,
            "COMMENT": _do_nothing,
            "COMPONENT-COEFFICIENTS": _do_nothing,
            "COMPONENT-OF": _do_nothing,
            "COMPONENTS": _add_component,
            "CONSENSUS-SEQUENCE": _do_nothing,
            "COPY-NUMBER": _do_nothing,
            "CREDITS": _do_nothing,
            "DATA-SOURCE": _do_nothing,
            "DBLINKS": _do_nothing,
            "DNA-FOOTPRINT-SIZE": _do_nothing,
            "DOCUMENTATION": _do_nothing,
            "ENZYME-NOT-USED-IN": _do_nothing,
            "EXPRESSION-MECHANISM": _do_nothing,
            "FAST-EQUILIBRATING-INSTANCES?": _do_nothing,
            "FEATURES": _do_nothing,
            "FUNCTIONAL-ASSIGNMENT-COMMENT": _do_nothing,
            "FUNCTIONAL-ASSIGNMENT-STATUS": _do_nothing,
            "GENE": _do_nothing,
            "GIBBS-0": _do_nothing,
            "GO-TERMS": _do_nothing,
            "GROUP-COORDS-2D": _do_nothing,
            "HAS-NO-STRUCTURE?": _do_nothing,
            "HIDE-SLOT?": _do_nothing,
            "IN-MIXTURE": _do_nothing,
            "INCHI": _do_nothing,
            "INCHI-KEY": _do_nothing,
            "INSTANCE-NAME-TEMPLATE": _do_nothing,
            "INTERNALS-OF-GROUP": _do_nothing,
            "ISOZYME-SEQUENCE-SIMILARITY": _do_nothing,
            "LOCATIONS": _do_nothing,
            "MEMBER-SORT-FN": _do_nothing,
            "MODIFIED-FORM": _do_nothing,
            "MOLECULAR-WEIGHT": _do_nothing,
            "MOLECULAR-WEIGHT-EXP": _do_nothing,
            "MOLECULAR-WEIGHT-KD": _do_nothing,
            "MOLECULAR-WEIGHT-SEQ": _do_nothing,
            "MONOISOTOPIC-MW": _do_nothing,
            "N+1-NAME": _do_nothing,
            "N-1-NAME": _do_nothing,
            "N-NAME": _do_nothing,
            "NEIDHARDT-SPOT-NUMBER": _do_nothing,
            "NON-STANDARD-INCHI": _do_nothing,
            "PATHOLOGIC-NAME-MATCHER-EVIDENCE": _do_nothing,
            "PATHOLOGIC-PWY-EVIDENCE": _do_nothing,
            "PI": _do_nothing,
            "PKA1": _do_nothing,
            "PKA2": _do_nothing,
            "PKA3": _do_nothing,
            "PROMOTER-BOX-NAME-1": _do_nothing,
            "PROMOTER-BOX-NAME-2": _do_nothing,
            "RADICAL-ATOMS": _do_nothing,
            "RECOGNIZED-PROMOTERS": _do_nothing,
            "REGULATED-BY": _do_nothing,
            "REGULATES": _do_nothing,
            "SMILES": _do_nothing,
            "SPECIES": _do_nothing,
            "SPLICE-FORM-INTRONS": _do_nothing,
            "STRUCTURE-BONDS": _do_nothing,
            "STRUCTURE-GROUPS": _do_nothing,
            "STRUCTURE-LINKS": _do_nothing,
            "SUPERATOMS": _do_nothing,
            "SYMMETRY": _do_nothing,
            "SYNONYMS": _do_nothing,
            "SYSTEMATIC-NAME": _do_nothing,
            "TAUTOMERS": _do_nothing,
            "UNMODIFIED-FORM": _do_nothing,
        }

    def parse(self) -> Tuple[Set[str], Dict[str, Set[str]]]:
        """Parse."""
        id_ = ""
        proteins: Dict[str, Set[str]] = {}
        monomers: Set[str] = set()
        complexes: Dict[str, Set[str]] = dict()
        for i, line in enumerate(self.file, self.start_idx):
            if any(line.startswith(i) for i in MALFORMED_LINE_STARTS):
                continue
            else:
                try:
                    identifier, content = line.rstrip().split(" - ", maxsplit=1)
                    if identifier == "UNIQUE-ID":
                        id_ = content
                        proteins[id_] = set()
                    elif not identifier.startswith("^"):
                        try:
                            self.actions[identifier](proteins, id_, content)
                        except KeyError:
                            logger.info(f"Unknown identifier {identifier} for protein {id_}")
                except ValueError:
                    logger.info(f"Malformed line {i} in proteins.dat")
        for k, v in proteins.items():
            if bool(v):
                complexes[k] = v
            else:
                monomers.add(k)
        return monomers, complexes
