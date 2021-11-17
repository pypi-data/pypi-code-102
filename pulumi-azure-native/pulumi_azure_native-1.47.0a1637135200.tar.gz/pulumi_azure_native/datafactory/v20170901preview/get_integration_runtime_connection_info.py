# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetIntegrationRuntimeConnectionInfoResult',
    'AwaitableGetIntegrationRuntimeConnectionInfoResult',
    'get_integration_runtime_connection_info',
    'get_integration_runtime_connection_info_output',
]

@pulumi.output_type
class GetIntegrationRuntimeConnectionInfoResult:
    """
    Connection information for encrypting the on-premises data source credentials.
    """
    def __init__(__self__, host_service_uri=None, identity_cert_thumbprint=None, is_identity_cert_exprired=None, public_key=None, service_token=None, version=None):
        if host_service_uri and not isinstance(host_service_uri, str):
            raise TypeError("Expected argument 'host_service_uri' to be a str")
        pulumi.set(__self__, "host_service_uri", host_service_uri)
        if identity_cert_thumbprint and not isinstance(identity_cert_thumbprint, str):
            raise TypeError("Expected argument 'identity_cert_thumbprint' to be a str")
        pulumi.set(__self__, "identity_cert_thumbprint", identity_cert_thumbprint)
        if is_identity_cert_exprired and not isinstance(is_identity_cert_exprired, bool):
            raise TypeError("Expected argument 'is_identity_cert_exprired' to be a bool")
        pulumi.set(__self__, "is_identity_cert_exprired", is_identity_cert_exprired)
        if public_key and not isinstance(public_key, str):
            raise TypeError("Expected argument 'public_key' to be a str")
        pulumi.set(__self__, "public_key", public_key)
        if service_token and not isinstance(service_token, str):
            raise TypeError("Expected argument 'service_token' to be a str")
        pulumi.set(__self__, "service_token", service_token)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="hostServiceUri")
    def host_service_uri(self) -> str:
        """
        The on-premises integration runtime host URL.
        """
        return pulumi.get(self, "host_service_uri")

    @property
    @pulumi.getter(name="identityCertThumbprint")
    def identity_cert_thumbprint(self) -> str:
        """
        The integration runtime SSL certificate thumbprint. Click-Once application uses it to do server validation.
        """
        return pulumi.get(self, "identity_cert_thumbprint")

    @property
    @pulumi.getter(name="isIdentityCertExprired")
    def is_identity_cert_exprired(self) -> bool:
        """
        Whether the identity certificate is expired.
        """
        return pulumi.get(self, "is_identity_cert_exprired")

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> str:
        """
        The public key for encrypting a credential when transferring the credential to the integration runtime.
        """
        return pulumi.get(self, "public_key")

    @property
    @pulumi.getter(name="serviceToken")
    def service_token(self) -> str:
        """
        The token generated in service. Callers use this token to authenticate to integration runtime.
        """
        return pulumi.get(self, "service_token")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        The integration runtime version.
        """
        return pulumi.get(self, "version")


class AwaitableGetIntegrationRuntimeConnectionInfoResult(GetIntegrationRuntimeConnectionInfoResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIntegrationRuntimeConnectionInfoResult(
            host_service_uri=self.host_service_uri,
            identity_cert_thumbprint=self.identity_cert_thumbprint,
            is_identity_cert_exprired=self.is_identity_cert_exprired,
            public_key=self.public_key,
            service_token=self.service_token,
            version=self.version)


def get_integration_runtime_connection_info(factory_name: Optional[str] = None,
                                            integration_runtime_name: Optional[str] = None,
                                            resource_group_name: Optional[str] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIntegrationRuntimeConnectionInfoResult:
    """
    Connection information for encrypting the on-premises data source credentials.


    :param str factory_name: The factory name.
    :param str integration_runtime_name: The integration runtime name.
    :param str resource_group_name: The resource group name.
    """
    __args__ = dict()
    __args__['factoryName'] = factory_name
    __args__['integrationRuntimeName'] = integration_runtime_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:datafactory/v20170901preview:getIntegrationRuntimeConnectionInfo', __args__, opts=opts, typ=GetIntegrationRuntimeConnectionInfoResult).value

    return AwaitableGetIntegrationRuntimeConnectionInfoResult(
        host_service_uri=__ret__.host_service_uri,
        identity_cert_thumbprint=__ret__.identity_cert_thumbprint,
        is_identity_cert_exprired=__ret__.is_identity_cert_exprired,
        public_key=__ret__.public_key,
        service_token=__ret__.service_token,
        version=__ret__.version)


@_utilities.lift_output_func(get_integration_runtime_connection_info)
def get_integration_runtime_connection_info_output(factory_name: Optional[pulumi.Input[str]] = None,
                                                   integration_runtime_name: Optional[pulumi.Input[str]] = None,
                                                   resource_group_name: Optional[pulumi.Input[str]] = None,
                                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIntegrationRuntimeConnectionInfoResult]:
    """
    Connection information for encrypting the on-premises data source credentials.


    :param str factory_name: The factory name.
    :param str integration_runtime_name: The integration runtime name.
    :param str resource_group_name: The resource group name.
    """
    ...
