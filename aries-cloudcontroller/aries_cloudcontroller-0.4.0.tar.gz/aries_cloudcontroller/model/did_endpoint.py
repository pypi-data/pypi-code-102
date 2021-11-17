# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401


class DIDEndpoint(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    DIDEndpoint - a model defined in OpenAPI
        did: DID of interest.
        endpoint: Endpoint to set (omit to delete) [Optional].
    """

    did: str
    endpoint: Optional[str] = None

    def __init__(
        self,
        *,
        did: str = None,
        endpoint: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            did=did,
            endpoint=endpoint,
            **kwargs,
        )

    @validator("did")
    def did_pattern(cls, value):

        pattern = r"^(did:sov:)?[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{21,22}$"
        if not re.match(pattern, value):
            raise ValueError(f"Value of did does not match regex pattern ('{pattern}')")
        return value

    @validator("endpoint")
    def endpoint_pattern(cls, value):
        # Property is optional
        if value is None:
            return

        pattern = r"^[A-Za-z0-9\.\-\+]+:\/\/([A-Za-z0-9][.A-Za-z0-9-_]+[A-Za-z0-9])+(:[1-9][0-9]*)?(\/[^?&#]+)?$"
        if not re.match(pattern, value):
            raise ValueError(
                f"Value of endpoint does not match regex pattern ('{pattern}')"
            )
        return value

    class Config:
        allow_population_by_field_name = True


DIDEndpoint.update_forward_refs()
