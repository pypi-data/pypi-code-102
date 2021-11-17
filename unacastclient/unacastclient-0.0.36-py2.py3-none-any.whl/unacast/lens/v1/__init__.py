# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: unacast/lens/v1/lens.proto, unacast/lens/v1/lens_service.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List, Optional

import betterproto
import grpclib


@dataclass(eq=False, repr=False)
class Lens(betterproto.Message):
    id: str = betterproto.string_field(1)
    catalog_id: str = betterproto.string_field(2)
    metric_id: str = betterproto.string_field(3)
    billing_account_id: str = betterproto.string_field(4)
    creator_email: str = betterproto.string_field(5)
    lens_filters: "__filter_v1__.RequestFilter" = betterproto.message_field(6)
    display_name: str = betterproto.string_field(10)
    description: str = betterproto.string_field(11)
    update_time_string: str = betterproto.string_field(13)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class DeleteLensRequest(betterproto.Message):
    billing_context: str = betterproto.string_field(1)
    lens_id: str = betterproto.string_field(2)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class ListLensesRequest(betterproto.Message):
    catalog_id: str = betterproto.string_field(1)
    billing_context: str = betterproto.string_field(2)
    creator_email_filter: str = betterproto.string_field(3)
    metric_id_filter: List[str] = betterproto.string_field(4)
    page_size: int = betterproto.int32_field(5)
    page_token: str = betterproto.string_field(6)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class ListLensesResponse(betterproto.Message):
    lenses: List["Lens"] = betterproto.message_field(1)
    response_size: int = betterproto.int32_field(2)
    next_page_token: str = betterproto.string_field(6)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class GetLensRequest(betterproto.Message):
    billing_context: str = betterproto.string_field(1)
    lens_id: str = betterproto.string_field(2)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class CreateLensRequest(betterproto.Message):
    catalog_id: str = betterproto.string_field(2)
    metric_id: str = betterproto.string_field(3)
    billing_account_id: str = betterproto.string_field(11)
    lens_filters: "__filter_v1__.RequestFilter" = betterproto.message_field(6)
    display_name: str = betterproto.string_field(9)
    description: str = betterproto.string_field(10)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class CreateLensResponse(betterproto.Message):
    lens: "Lens" = betterproto.message_field(1)

    def __post_init__(self) -> None:
        super().__post_init__()


class LensServiceStub(betterproto.ServiceStub):
    async def create_lens(
        self,
        *,
        catalog_id: str = "",
        metric_id: str = "",
        billing_account_id: str = "",
        lens_filters: "__filter_v1__.RequestFilter" = None,
        display_name: str = "",
        description: str = "",
    ) -> "CreateLensResponse":

        request = CreateLensRequest()
        request.catalog_id = catalog_id
        request.metric_id = metric_id
        request.billing_account_id = billing_account_id
        if lens_filters is not None:
            request.lens_filters = lens_filters
        request.display_name = display_name
        request.description = description

        return await self._unary_unary(
            "/unacast.lens.v1.LensService/CreateLens", request, CreateLensResponse
        )

    async def get_lens(self, *, billing_context: str = "", lens_id: str = "") -> "Lens":

        request = GetLensRequest()
        request.billing_context = billing_context
        request.lens_id = lens_id

        return await self._unary_unary(
            "/unacast.lens.v1.LensService/GetLens", request, Lens
        )

    async def list_lenses(
        self,
        *,
        catalog_id: str = "",
        billing_context: str = "",
        creator_email_filter: str = "",
        metric_id_filter: Optional[List[str]] = None,
        page_size: int = 0,
        page_token: str = "",
    ) -> "ListLensesResponse":
        metric_id_filter = metric_id_filter or []

        request = ListLensesRequest()
        request.catalog_id = catalog_id
        request.billing_context = billing_context
        request.creator_email_filter = creator_email_filter
        request.metric_id_filter = metric_id_filter
        request.page_size = page_size
        request.page_token = page_token

        return await self._unary_unary(
            "/unacast.lens.v1.LensService/ListLenses", request, ListLensesResponse
        )

    async def delete_lens(
        self, *, billing_context: str = "", lens_id: str = ""
    ) -> "betterproto_lib_google_protobuf.Empty":

        request = DeleteLensRequest()
        request.billing_context = billing_context
        request.lens_id = lens_id

        return await self._unary_unary(
            "/unacast.lens.v1.LensService/DeleteLens",
            request,
            betterproto_lib_google_protobuf.Empty,
        )


from ...filter import v1 as __filter_v1__
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
