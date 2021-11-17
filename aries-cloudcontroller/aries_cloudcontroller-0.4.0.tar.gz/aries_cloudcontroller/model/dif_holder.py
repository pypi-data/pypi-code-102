# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401


class DIFHolder(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    DIFHolder - a model defined in OpenAPI
        directive: Preference [Optional].
        field_id: The field_id of this DIFHolder [Optional].
    """

    directive: Optional[Literal["required", "preferred"]] = None
    field_id: Optional[List[str]] = None

    def __init__(
        self,
        *,
        directive: Optional[Literal["required", "preferred"]] = None,
        field_id: Optional[List[str]] = None,
        **kwargs,
    ):
        super().__init__(
            directive=directive,
            field_id=field_id,
            **kwargs,
        )

    class Config:
        allow_population_by_field_name = True


DIFHolder.update_forward_refs()
