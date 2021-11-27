from typing import Optional, List

from camel_model.camel_model import CamelModel

from domain.power_supply.power_supply_component import PowerSupplyComponent
from domain.electronic.electronic_element import ElectronicElement

from domain.engine.engine_section import EngineSection
from domain.frame.frame_element import FrameElement
from domain.generic_replacements.replacement import Replacement
from domain.tightening_specifications.specification_element import SpecificationElement


class MotorcycleModel(CamelModel):
    model_name: str
    generic_replacements: Optional[List[Replacement]]
    tightening_specifications: Optional[List[SpecificationElement]]
    electronic: Optional[List[ElectronicElement]]
    engine: Optional[List[EngineSection]]
    frame: Optional[List[FrameElement]]
    power_supply: Optional[List[PowerSupplyComponent]]
