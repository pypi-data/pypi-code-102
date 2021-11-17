# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing
# Export this package's modules as members:
from ._enums import *
from .container_group import *
from .get_container_group import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.containerinstance.v20170801preview as __v20170801preview
    v20170801preview = __v20170801preview
    import pulumi_azure_native.containerinstance.v20171001preview as __v20171001preview
    v20171001preview = __v20171001preview
    import pulumi_azure_native.containerinstance.v20171201preview as __v20171201preview
    v20171201preview = __v20171201preview
    import pulumi_azure_native.containerinstance.v20180201preview as __v20180201preview
    v20180201preview = __v20180201preview
    import pulumi_azure_native.containerinstance.v20180401 as __v20180401
    v20180401 = __v20180401
    import pulumi_azure_native.containerinstance.v20180601 as __v20180601
    v20180601 = __v20180601
    import pulumi_azure_native.containerinstance.v20180901 as __v20180901
    v20180901 = __v20180901
    import pulumi_azure_native.containerinstance.v20181001 as __v20181001
    v20181001 = __v20181001
    import pulumi_azure_native.containerinstance.v20191201 as __v20191201
    v20191201 = __v20191201
    import pulumi_azure_native.containerinstance.v20201101 as __v20201101
    v20201101 = __v20201101
    import pulumi_azure_native.containerinstance.v20210301 as __v20210301
    v20210301 = __v20210301
    import pulumi_azure_native.containerinstance.v20210701 as __v20210701
    v20210701 = __v20210701
    import pulumi_azure_native.containerinstance.v20210901 as __v20210901
    v20210901 = __v20210901
else:
    v20170801preview = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20170801preview')
    v20171001preview = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20171001preview')
    v20171201preview = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20171201preview')
    v20180201preview = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20180201preview')
    v20180401 = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20180401')
    v20180601 = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20180601')
    v20180901 = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20180901')
    v20181001 = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20181001')
    v20191201 = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20191201')
    v20201101 = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20201101')
    v20210301 = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20210301')
    v20210701 = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20210701')
    v20210901 = _utilities.lazy_import('pulumi_azure_native.containerinstance.v20210901')

