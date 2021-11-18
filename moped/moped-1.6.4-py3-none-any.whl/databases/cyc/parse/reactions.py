from __future__ import annotations

import logging
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict

from ..data import ParseReaction
from .shared import (
    MALFORMED_LINE_STARTS,
    _add_database_link,
    _add_type,
    _do_nothing,
    _open_file_and_remove_comments,
    _rename,
    _set_gibbs0,
    _set_name,
)

logger = logging.getLogger(__name__)


def _set_ec_number(reactions: Dict[str, ParseReaction], id_: str, ec_number: str) -> None:
    reactions[id_].ec = ec_number


def _add_reaction_pathway(reactions: Dict[str, ParseReaction], id_: str, pathway: str) -> None:
    reactions[id_].pathways.add(pathway)


def _add_reaction_enzyme(reactions: Dict[str, ParseReaction], id_: str, enzyme: str) -> None:
    reactions[id_].enzymes.add(enzyme)


def _set_reaction_direction(reactions: Dict[str, ParseReaction], id_: str, direction: str) -> None:
    reactions[id_].direction = direction
    if direction == "REVERSIBLE":
        reactions[id_].reversible = True
    else:
        reactions[id_].reversible = False


def _add_reaction_location(reactions: Dict[str, ParseReaction], id_: str, location: str) -> None:
    location = location.replace("CCI-", "CCO-")
    if location.startswith("CCO-"):
        reactions[id_].locations.append(location)


def _set_substrate(
    reactions: Dict[str, ParseReaction],
    id_: str,
    substrate: str,
    type_map: Dict[str, str],
) -> None:
    substrate = _rename(type_map.get(substrate, substrate)) + "_c"
    reactions[id_].substrates[substrate] = -1
    reactions[id_].substrate_compartments[substrate] = "CCO-IN"


def _set_product(
    reactions: Dict[str, ParseReaction],
    id_: str,
    product: str,
    type_map: Dict[str, str],
) -> None:
    product = _rename(type_map.get(product, product)) + "_c"
    reactions[id_].products[product] = 1
    reactions[id_].product_compartments[product] = "CCO-IN"


def _set_substrate_coefficient(
    reactions: Dict[str, ParseReaction],
    id_: str,
    coefficient: str,
    substrate: str,
    type_map: Dict[str, str],
) -> None:
    try:
        reactions[id_].substrates[_rename(type_map.get(substrate, substrate)) + "_c"] = -float(coefficient)
    except ValueError:
        pass


def _set_product_coefficient(
    reactions: Dict[str, ParseReaction],
    id_: str,
    coefficient: str,
    product: str,
    type_map: Dict[str, str],
) -> None:
    try:
        reactions[id_].products[_rename(type_map.get(product, product)) + "_c"] = float(coefficient)
    except ValueError:
        pass


def _set_substrate_compartment(
    reactions: Dict[str, ParseReaction],
    id_: str,
    compartment: str,
    substrate: str,
    type_map: Dict[str, str],
) -> None:
    substrate = _rename(type_map.get(substrate, substrate)) + "_c"
    if compartment == "CCO-OUT":
        reactions[id_].substrate_compartments[substrate] = compartment
    elif compartment == "CCO-MIDDLE":
        reactions[id_].substrate_compartments[substrate] = "CCO-OUT"
    else:
        # reactions[id_].product_compartments[substrate] = "CCO-OUT"
        logger.info(f"Unknown compartment {compartment}")


def _set_product_compartment(
    reactions: Dict[str, ParseReaction],
    id_: str,
    compartment: str,
    product: str,
    type_map: Dict[str, str],
) -> None:
    product = _rename(type_map.get(product, product)) + "_c"
    if compartment == "CCO-OUT":
        reactions[id_].product_compartments[product] = compartment
    elif compartment == "CCO-MIDDLE":
        reactions[id_].product_compartments[product] = "CCO-OUT"
    else:
        # reactions[id_].product_compartments[product] = "CCO-OUT"
        logger.info(f"Unknown compartment {compartment}")


class ReactionParser:
    """Reaction Parser."""

    def __init__(self, path: Path, type_map: Dict[str, str]) -> None:
        """Parse reactions and pathways."""
        file, start_idx = _open_file_and_remove_comments(path)
        self.file = file
        self.start_idx = start_idx
        self.type_map = type_map

        self.actions: Dict[str, Callable[[Any, Any, Any], None]] = {
            "TYPES": partial(_add_type, type_map=self.type_map),
            "COMMON-NAME": _set_name,
            "ATOM-MAPPINGS": _do_nothing,
            "CANNOT-BALANCE?": _do_nothing,
            "CITATIONS": _do_nothing,
            "COMMENT": _do_nothing,
            "CREDITS": _do_nothing,
            "DATA-SOURCE": _do_nothing,
            "DBLINKS": _add_database_link,
            "DOCUMENTATION": _do_nothing,
            "EC-NUMBER": _set_ec_number,
            "ENZYMATIC-REACTION": _add_reaction_enzyme,
            "ENZYMES-NOT-USED": _do_nothing,
            "EQUILIBRIUM-CONSTANT": _do_nothing,
            "GIBBS-0": _set_gibbs0,
            "HIDE-SLOT?": _do_nothing,
            "IN-PATHWAY": _add_reaction_pathway,
            "INSTANCE-NAME-TEMPLATE": _do_nothing,
            "LEFT": partial(_set_substrate, type_map=self.type_map),
            "MEMBER-SORT-FN": _do_nothing,
            "ORPHAN?": _do_nothing,
            "PATHOLOGIC-NAME-MATCHER-EVIDENCE": _do_nothing,
            "PATHOLOGIC-PWY-EVIDENCE": _do_nothing,
            "PHYSIOLOGICALLY-RELEVANT?": _do_nothing,
            "PREDECESSORS": _do_nothing,
            "PRIMARIES": _do_nothing,
            "REACTION-BALANCE-STATUS": _do_nothing,
            "REACTION-DIRECTION": _set_reaction_direction,
            "REACTION-LIST": _do_nothing,
            "REGULATED-BY": _do_nothing,
            "REQUIREMENTS": _do_nothing,
            "RIGHT": partial(_set_product, type_map=self.type_map),
            "RXN-LOCATIONS": _add_reaction_location,
            "SIGNAL": _do_nothing,
            "SPECIES": _do_nothing,
            "SPONTANEOUS?": _do_nothing,
            "STD-REDUCTION-POTENTIAL": _do_nothing,
            "SYNONYMS": _do_nothing,
            "SYSTEMATIC-NAME": _do_nothing,
            "TAXONOMIC-RANGE": _do_nothing,
        }

        self.sub_actions: Dict[str, Dict[str, Callable[[Any, Any, Any, Any], None]]] = {
            "^COMPARTMENT": {
                "LEFT": partial(_set_substrate_compartment, type_map=self.type_map),
                "RIGHT": lambda a, b, c, d: _set_product_compartment(a, b, c, d, type_map=self.type_map),
            },
            "^OFFICIAL?": {
                "EC-NUMBER": _do_nothing,
            },
            "^COEFFICIENT": {
                "LEFT": lambda a, b, c, d: _set_substrate_coefficient(a, b, c, d, type_map=self.type_map),
                "RIGHT": lambda a, b, c, d: _set_product_coefficient(a, b, c, d, type_map=self.type_map),
            },
        }

    def parse(self) -> Dict[str, ParseReaction]:
        """Parse."""
        id_ = ""
        reactions = {}
        for line in self.file:
            if any(line.startswith(i) for i in MALFORMED_LINE_STARTS):
                continue
            else:
                identifier, content = line.rstrip().split(" - ", maxsplit=1)
                if identifier == "UNIQUE-ID":
                    id_ = content
                    reactions[id_] = ParseReaction(id=id_, base_id=id_)

                elif not identifier.startswith("^"):
                    try:
                        self.actions[identifier](reactions, id_, content)
                        last_identifier = identifier
                        last_content = content
                    except KeyError:
                        logger.info(f"Unknown identifier {identifier} for reaction {id_}")
                else:
                    self.sub_actions[identifier][last_identifier](reactions, id_, content, last_content)
        return reactions
