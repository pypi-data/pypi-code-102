from __future__ import annotations

import logging
from collections import defaultdict
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

from ..data import ParseCompound
from .shared import (
    MALFORMED_LINE_STARTS,
    _add_database_link,
    _add_type,
    _do_nothing,
    _open_file_and_remove_comments,
    _set_gibbs0,
    _set_name,
)

logger = logging.getLogger(__name__)


def _set_atom_charges(compounds: Dict[str, ParseCompound], id_: str, content: str) -> None:
    """Short description.

    Parameters
    ----------
    Compounds : dict
    id_ : str
    content : str(int int)
        Are of form "(8 -1)", we only need the second part
    """
    compounds[id_].charge += int(content[1:-1].split()[-1])


def _set_chemical_formula(compounds: Dict[str, ParseCompound], id_: str, content: str) -> None:
    """Short description.

    Parameters
    ----------
    Compounds : dict
    id_ : str
    content : str(int int)
        Are of form (C 11)
    """
    atom, count = content[1:-1].split(" ")
    compounds[id_].formula[atom] = int(count)


def _set_smiles(compounds: Dict[str, ParseCompound], id_: str, content: str) -> None:
    """Short description.

    Parameters
    ----------
    Compounds : dict
    id_ : str
    content : str
    """
    compounds[id_].smiles = content


class CompoundParser:
    """Class to parse compounds."""

    def __init__(self, path: Path, type_map: Dict[str, str]) -> None:
        """Parser compound information."""
        file, start_idx = _open_file_and_remove_comments(path)
        self.file = file
        self.start_idx = start_idx
        self.type_map = type_map

        self.actions: Dict[str, Callable[[Any, Any, Any], None]] = {
            "TYPES": partial(_add_type, type_map=self.type_map),
            "COMMON-NAME": _set_name,
            "ABBREV-NAME": _do_nothing,
            "ACCESSION-1": _do_nothing,
            "ANTICODON": _do_nothing,
            "ATOM-CHARGES": _set_atom_charges,
            "ATOM-ISOTOPES": _do_nothing,
            "CATALYZES": _do_nothing,
            "CFG-ICON-COLOR": _do_nothing,
            "CHEMICAL-FORMULA": _set_chemical_formula,
            "CITATIONS": _do_nothing,
            "CODING-SEGMENTS": _do_nothing,
            "CODONS": _do_nothing,
            "COFACTORS-OF": _do_nothing,
            "COMMENT": _do_nothing,
            "COMPONENT-COEFFICIENTS": _do_nothing,
            "COMPONENT-OF": _do_nothing,
            "COMPONENTS": _do_nothing,
            "CONSENSUS-SEQUENCE": _do_nothing,
            "COPY-NUMBER": _do_nothing,
            "CREDITS": _do_nothing,
            "DATA-SOURCE": _do_nothing,
            "DBLINKS": _add_database_link,
            "DNA-FOOTPRINT-SIZE": _do_nothing,
            "DOCUMENTATION": _do_nothing,
            "ENZYME-NOT-USED-IN": _do_nothing,
            "EXPRESSION-MECHANISM": _do_nothing,
            "FAST-EQUILIBRATING-INSTANCES?": _do_nothing,
            "FEATURES": _do_nothing,
            "FUNCTIONAL-ASSIGNMENT-COMMENT": _do_nothing,
            "FUNCTIONAL-ASSIGNMENT-STATUS": _do_nothing,
            "GENE": _do_nothing,
            "GIBBS-0": _set_gibbs0,
            "GO-TERMS": _do_nothing,
            "GROUP-COORDS-2D": _do_nothing,
            "GROUP-INTERNALS": _do_nothing,
            "HAS-NO-STRUCTURE?": _do_nothing,
            "HIDE-SLOT?": _do_nothing,
            "IN-MIXTURE": _do_nothing,
            "INCHI": _do_nothing,
            "INCHI-KEY": _do_nothing,
            "INSTANCE-NAME-TEMPLATE": _do_nothing,
            "INTERNALS-OF-GROUP": _do_nothing,
            "ISOZYME-SEQUENCE-SIMILARITY": _do_nothing,
            "LEFT-END-POSITION": _do_nothing,
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
            "RADICAL-ATOMS": _do_nothing,
            "REGULATED-BY": _do_nothing,
            "REGULATES": _do_nothing,
            "RIGHT-END-POSITION": _do_nothing,
            "SMILES": _set_smiles,
            "SPECIES": _do_nothing,
            "SPLICE-FORM-INTRONS": _do_nothing,
            "STRUCTURE-GROUPS": _do_nothing,
            "STRUCTURE-LINKS": _do_nothing,
            "SUPERATOMS": _do_nothing,
            "SYMMETRY": _do_nothing,
            "SYNONYMS": _do_nothing,
            "SYSTEMATIC-NAME": _do_nothing,
            "TAUTOMERS": _do_nothing,
            "UNMODIFIED-FORM": _do_nothing,
            "LOGP": _do_nothing,
            "POLAR-SURFACE-AREA": _do_nothing,
        }

    @staticmethod
    def gather_compound_types(compounds: Dict[str, ParseCompound]) -> Dict[str, List[str]]:
        """Return (type: list(cpds)) dictionary.

        Only uses the highest-level type
        """
        types = defaultdict(list)
        for id_, cpd in compounds.items():
            if bool(cpd.types):
                # Only use highest level
                types[cpd.types[-1] + "_c"].append(id_)
        return dict(types)

    def parse(self) -> Tuple[Dict[str, ParseCompound], Dict[str, List[str]]]:
        """Parse."""
        compounds: Dict[str, ParseCompound] = {}
        for line in self.file:
            if any(line.startswith(i) for i in MALFORMED_LINE_STARTS):
                continue
            else:
                identifier, content = line.rstrip().split(" - ", maxsplit=1)
                if identifier == "UNIQUE-ID":
                    base_id = content
                    id_ = content + "_c"
                    compounds[id_] = ParseCompound(
                        id=id_,
                        base_id=base_id,
                        compartment="CYTOSOL",
                    )
                else:
                    try:
                        self.actions[identifier](compounds, id_, content)
                    except KeyError:
                        logger.info(f"Unknown identifier {identifier} for compound {id_}")
        compound_types = self.gather_compound_types(compounds)
        return compounds, compound_types
