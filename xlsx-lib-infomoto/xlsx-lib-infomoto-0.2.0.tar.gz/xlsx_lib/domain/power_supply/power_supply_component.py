from typing import List, Optional

from camel_model.camel_model import CamelModel

from domain.power_supply.component_attribute import ComponentAttribute


class PowerSupplyComponent(CamelModel):
    name: str
    value: Optional[str]
    observations: Optional[str]
    component_attributes: Optional[List[ComponentAttribute]]