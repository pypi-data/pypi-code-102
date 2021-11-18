"""Format the Generated Namecodes for Markdown Presentation"""

from snakemd import Document

from nautilus_namecodes.namecodes_dataclasses import (
    AllCodes,
    BlockCodes,
    PlaneCodes,
    SectionCodes,
)
from nautilus_namecodes.scheme.v_0_0_1.namecodes import AllNameCodes


class MarkdownOutput:
    """Generate Markdown Formatted Codes."""

    def __init__(self) -> None:
        self.all_name_codes: AllCodes = AllNameCodes().get_all_codes

        self.doc = Document(f"Nautilus_Namecodes_{self.all_name_codes.scheme_version}")
