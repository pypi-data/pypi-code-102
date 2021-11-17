# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['ManagedInstanceArgs', 'ManagedInstance']

@pulumi.input_type
class ManagedInstanceArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 administrator_login: Optional[pulumi.Input[str]] = None,
                 administrator_login_password: Optional[pulumi.Input[str]] = None,
                 collation: Optional[pulumi.Input[str]] = None,
                 dns_zone_partner: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input['ResourceIdentityArgs']] = None,
                 instance_pool_id: Optional[pulumi.Input[str]] = None,
                 license_type: Optional[pulumi.Input[Union[str, 'ManagedInstanceLicenseType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 managed_instance_create_mode: Optional[pulumi.Input[Union[str, 'ManagedServerCreateMode']]] = None,
                 managed_instance_name: Optional[pulumi.Input[str]] = None,
                 minimal_tls_version: Optional[pulumi.Input[str]] = None,
                 proxy_override: Optional[pulumi.Input[Union[str, 'ManagedInstanceProxyOverride']]] = None,
                 public_data_endpoint_enabled: Optional[pulumi.Input[bool]] = None,
                 restore_point_in_time: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['SkuArgs']] = None,
                 source_managed_instance_id: Optional[pulumi.Input[str]] = None,
                 storage_size_in_gb: Optional[pulumi.Input[int]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timezone_id: Optional[pulumi.Input[str]] = None,
                 v_cores: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a ManagedInstance resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] administrator_login: Administrator username for the managed instance. Can only be specified when the managed instance is being created (and is required for creation).
        :param pulumi.Input[str] administrator_login_password: The administrator login password (required for managed instance creation).
        :param pulumi.Input[str] collation: Collation of the managed instance.
        :param pulumi.Input[str] dns_zone_partner: The resource id of another managed instance whose DNS zone this managed instance will share after creation.
        :param pulumi.Input['ResourceIdentityArgs'] identity: The Azure Active Directory identity of the managed instance.
        :param pulumi.Input[str] instance_pool_id: The Id of the instance pool this managed server belongs to.
        :param pulumi.Input[Union[str, 'ManagedInstanceLicenseType']] license_type: The license type. Possible values are 'LicenseIncluded' (regular price inclusive of a new SQL license) and 'BasePrice' (discounted AHB price for bringing your own SQL licenses).
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] maintenance_configuration_id: Specifies maintenance configuration id to apply to this managed instance.
        :param pulumi.Input[Union[str, 'ManagedServerCreateMode']] managed_instance_create_mode: Specifies the mode of database creation.
               
               Default: Regular instance creation.
               
               Restore: Creates an instance by restoring a set of backups to specific point in time. RestorePointInTime and SourceManagedInstanceId must be specified.
        :param pulumi.Input[str] managed_instance_name: The name of the managed instance.
        :param pulumi.Input[str] minimal_tls_version: Minimal TLS version. Allowed values: 'None', '1.0', '1.1', '1.2'
        :param pulumi.Input[Union[str, 'ManagedInstanceProxyOverride']] proxy_override: Connection type used for connecting to the instance.
        :param pulumi.Input[bool] public_data_endpoint_enabled: Whether or not the public data endpoint is enabled.
        :param pulumi.Input[str] restore_point_in_time: Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database.
        :param pulumi.Input['SkuArgs'] sku: Managed instance SKU. Allowed values for sku.name: GP_Gen4, GP_Gen5, BC_Gen4, BC_Gen5
        :param pulumi.Input[str] source_managed_instance_id: The resource identifier of the source managed instance associated with create operation of this instance.
        :param pulumi.Input[int] storage_size_in_gb: Storage size in GB. Minimum value: 32. Maximum value: 8192. Increments of 32 GB allowed only.
        :param pulumi.Input[str] subnet_id: Subnet resource ID for the managed instance.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] timezone_id: Id of the timezone. Allowed values are timezones supported by Windows.
               Windows keeps details on supported timezones, including the id, in registry under
               KEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Time Zones.
               You can get those registry values via SQL Server by querying SELECT name AS timezone_id FROM sys.time_zone_info.
               List of Ids can also be obtained by executing [System.TimeZoneInfo]::GetSystemTimeZones() in PowerShell.
               An example of valid timezone id is "Pacific Standard Time" or "W. Europe Standard Time".
        :param pulumi.Input[int] v_cores: The number of vCores. Allowed values: 8, 16, 24, 32, 40, 64, 80.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if administrator_login is not None:
            pulumi.set(__self__, "administrator_login", administrator_login)
        if administrator_login_password is not None:
            pulumi.set(__self__, "administrator_login_password", administrator_login_password)
        if collation is not None:
            pulumi.set(__self__, "collation", collation)
        if dns_zone_partner is not None:
            pulumi.set(__self__, "dns_zone_partner", dns_zone_partner)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if instance_pool_id is not None:
            pulumi.set(__self__, "instance_pool_id", instance_pool_id)
        if license_type is not None:
            pulumi.set(__self__, "license_type", license_type)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if maintenance_configuration_id is not None:
            pulumi.set(__self__, "maintenance_configuration_id", maintenance_configuration_id)
        if managed_instance_create_mode is not None:
            pulumi.set(__self__, "managed_instance_create_mode", managed_instance_create_mode)
        if managed_instance_name is not None:
            pulumi.set(__self__, "managed_instance_name", managed_instance_name)
        if minimal_tls_version is not None:
            pulumi.set(__self__, "minimal_tls_version", minimal_tls_version)
        if proxy_override is not None:
            pulumi.set(__self__, "proxy_override", proxy_override)
        if public_data_endpoint_enabled is not None:
            pulumi.set(__self__, "public_data_endpoint_enabled", public_data_endpoint_enabled)
        if restore_point_in_time is not None:
            pulumi.set(__self__, "restore_point_in_time", restore_point_in_time)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if source_managed_instance_id is not None:
            pulumi.set(__self__, "source_managed_instance_id", source_managed_instance_id)
        if storage_size_in_gb is not None:
            pulumi.set(__self__, "storage_size_in_gb", storage_size_in_gb)
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if timezone_id is not None:
            pulumi.set(__self__, "timezone_id", timezone_id)
        if v_cores is not None:
            pulumi.set(__self__, "v_cores", v_cores)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="administratorLogin")
    def administrator_login(self) -> Optional[pulumi.Input[str]]:
        """
        Administrator username for the managed instance. Can only be specified when the managed instance is being created (and is required for creation).
        """
        return pulumi.get(self, "administrator_login")

    @administrator_login.setter
    def administrator_login(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "administrator_login", value)

    @property
    @pulumi.getter(name="administratorLoginPassword")
    def administrator_login_password(self) -> Optional[pulumi.Input[str]]:
        """
        The administrator login password (required for managed instance creation).
        """
        return pulumi.get(self, "administrator_login_password")

    @administrator_login_password.setter
    def administrator_login_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "administrator_login_password", value)

    @property
    @pulumi.getter
    def collation(self) -> Optional[pulumi.Input[str]]:
        """
        Collation of the managed instance.
        """
        return pulumi.get(self, "collation")

    @collation.setter
    def collation(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "collation", value)

    @property
    @pulumi.getter(name="dnsZonePartner")
    def dns_zone_partner(self) -> Optional[pulumi.Input[str]]:
        """
        The resource id of another managed instance whose DNS zone this managed instance will share after creation.
        """
        return pulumi.get(self, "dns_zone_partner")

    @dns_zone_partner.setter
    def dns_zone_partner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dns_zone_partner", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ResourceIdentityArgs']]:
        """
        The Azure Active Directory identity of the managed instance.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ResourceIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter(name="instancePoolId")
    def instance_pool_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Id of the instance pool this managed server belongs to.
        """
        return pulumi.get(self, "instance_pool_id")

    @instance_pool_id.setter
    def instance_pool_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_pool_id", value)

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> Optional[pulumi.Input[Union[str, 'ManagedInstanceLicenseType']]]:
        """
        The license type. Possible values are 'LicenseIncluded' (regular price inclusive of a new SQL license) and 'BasePrice' (discounted AHB price for bringing your own SQL licenses).
        """
        return pulumi.get(self, "license_type")

    @license_type.setter
    def license_type(self, value: Optional[pulumi.Input[Union[str, 'ManagedInstanceLicenseType']]]):
        pulumi.set(self, "license_type", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies maintenance configuration id to apply to this managed instance.
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @maintenance_configuration_id.setter
    def maintenance_configuration_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "maintenance_configuration_id", value)

    @property
    @pulumi.getter(name="managedInstanceCreateMode")
    def managed_instance_create_mode(self) -> Optional[pulumi.Input[Union[str, 'ManagedServerCreateMode']]]:
        """
        Specifies the mode of database creation.
        
        Default: Regular instance creation.
        
        Restore: Creates an instance by restoring a set of backups to specific point in time. RestorePointInTime and SourceManagedInstanceId must be specified.
        """
        return pulumi.get(self, "managed_instance_create_mode")

    @managed_instance_create_mode.setter
    def managed_instance_create_mode(self, value: Optional[pulumi.Input[Union[str, 'ManagedServerCreateMode']]]):
        pulumi.set(self, "managed_instance_create_mode", value)

    @property
    @pulumi.getter(name="managedInstanceName")
    def managed_instance_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the managed instance.
        """
        return pulumi.get(self, "managed_instance_name")

    @managed_instance_name.setter
    def managed_instance_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "managed_instance_name", value)

    @property
    @pulumi.getter(name="minimalTlsVersion")
    def minimal_tls_version(self) -> Optional[pulumi.Input[str]]:
        """
        Minimal TLS version. Allowed values: 'None', '1.0', '1.1', '1.2'
        """
        return pulumi.get(self, "minimal_tls_version")

    @minimal_tls_version.setter
    def minimal_tls_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "minimal_tls_version", value)

    @property
    @pulumi.getter(name="proxyOverride")
    def proxy_override(self) -> Optional[pulumi.Input[Union[str, 'ManagedInstanceProxyOverride']]]:
        """
        Connection type used for connecting to the instance.
        """
        return pulumi.get(self, "proxy_override")

    @proxy_override.setter
    def proxy_override(self, value: Optional[pulumi.Input[Union[str, 'ManagedInstanceProxyOverride']]]):
        pulumi.set(self, "proxy_override", value)

    @property
    @pulumi.getter(name="publicDataEndpointEnabled")
    def public_data_endpoint_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not the public data endpoint is enabled.
        """
        return pulumi.get(self, "public_data_endpoint_enabled")

    @public_data_endpoint_enabled.setter
    def public_data_endpoint_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "public_data_endpoint_enabled", value)

    @property
    @pulumi.getter(name="restorePointInTime")
    def restore_point_in_time(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database.
        """
        return pulumi.get(self, "restore_point_in_time")

    @restore_point_in_time.setter
    def restore_point_in_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "restore_point_in_time", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuArgs']]:
        """
        Managed instance SKU. Allowed values for sku.name: GP_Gen4, GP_Gen5, BC_Gen4, BC_Gen5
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="sourceManagedInstanceId")
    def source_managed_instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The resource identifier of the source managed instance associated with create operation of this instance.
        """
        return pulumi.get(self, "source_managed_instance_id")

    @source_managed_instance_id.setter
    def source_managed_instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_managed_instance_id", value)

    @property
    @pulumi.getter(name="storageSizeInGB")
    def storage_size_in_gb(self) -> Optional[pulumi.Input[int]]:
        """
        Storage size in GB. Minimum value: 32. Maximum value: 8192. Increments of 32 GB allowed only.
        """
        return pulumi.get(self, "storage_size_in_gb")

    @storage_size_in_gb.setter
    def storage_size_in_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "storage_size_in_gb", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        Subnet resource ID for the managed instance.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="timezoneId")
    def timezone_id(self) -> Optional[pulumi.Input[str]]:
        """
        Id of the timezone. Allowed values are timezones supported by Windows.
        Windows keeps details on supported timezones, including the id, in registry under
        KEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Time Zones.
        You can get those registry values via SQL Server by querying SELECT name AS timezone_id FROM sys.time_zone_info.
        List of Ids can also be obtained by executing [System.TimeZoneInfo]::GetSystemTimeZones() in PowerShell.
        An example of valid timezone id is "Pacific Standard Time" or "W. Europe Standard Time".
        """
        return pulumi.get(self, "timezone_id")

    @timezone_id.setter
    def timezone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "timezone_id", value)

    @property
    @pulumi.getter(name="vCores")
    def v_cores(self) -> Optional[pulumi.Input[int]]:
        """
        The number of vCores. Allowed values: 8, 16, 24, 32, 40, 64, 80.
        """
        return pulumi.get(self, "v_cores")

    @v_cores.setter
    def v_cores(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "v_cores", value)


class ManagedInstance(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 administrator_login: Optional[pulumi.Input[str]] = None,
                 administrator_login_password: Optional[pulumi.Input[str]] = None,
                 collation: Optional[pulumi.Input[str]] = None,
                 dns_zone_partner: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ResourceIdentityArgs']]] = None,
                 instance_pool_id: Optional[pulumi.Input[str]] = None,
                 license_type: Optional[pulumi.Input[Union[str, 'ManagedInstanceLicenseType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 managed_instance_create_mode: Optional[pulumi.Input[Union[str, 'ManagedServerCreateMode']]] = None,
                 managed_instance_name: Optional[pulumi.Input[str]] = None,
                 minimal_tls_version: Optional[pulumi.Input[str]] = None,
                 proxy_override: Optional[pulumi.Input[Union[str, 'ManagedInstanceProxyOverride']]] = None,
                 public_data_endpoint_enabled: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 restore_point_in_time: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 source_managed_instance_id: Optional[pulumi.Input[str]] = None,
                 storage_size_in_gb: Optional[pulumi.Input[int]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timezone_id: Optional[pulumi.Input[str]] = None,
                 v_cores: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        An Azure SQL managed instance.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] administrator_login: Administrator username for the managed instance. Can only be specified when the managed instance is being created (and is required for creation).
        :param pulumi.Input[str] administrator_login_password: The administrator login password (required for managed instance creation).
        :param pulumi.Input[str] collation: Collation of the managed instance.
        :param pulumi.Input[str] dns_zone_partner: The resource id of another managed instance whose DNS zone this managed instance will share after creation.
        :param pulumi.Input[pulumi.InputType['ResourceIdentityArgs']] identity: The Azure Active Directory identity of the managed instance.
        :param pulumi.Input[str] instance_pool_id: The Id of the instance pool this managed server belongs to.
        :param pulumi.Input[Union[str, 'ManagedInstanceLicenseType']] license_type: The license type. Possible values are 'LicenseIncluded' (regular price inclusive of a new SQL license) and 'BasePrice' (discounted AHB price for bringing your own SQL licenses).
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] maintenance_configuration_id: Specifies maintenance configuration id to apply to this managed instance.
        :param pulumi.Input[Union[str, 'ManagedServerCreateMode']] managed_instance_create_mode: Specifies the mode of database creation.
               
               Default: Regular instance creation.
               
               Restore: Creates an instance by restoring a set of backups to specific point in time. RestorePointInTime and SourceManagedInstanceId must be specified.
        :param pulumi.Input[str] managed_instance_name: The name of the managed instance.
        :param pulumi.Input[str] minimal_tls_version: Minimal TLS version. Allowed values: 'None', '1.0', '1.1', '1.2'
        :param pulumi.Input[Union[str, 'ManagedInstanceProxyOverride']] proxy_override: Connection type used for connecting to the instance.
        :param pulumi.Input[bool] public_data_endpoint_enabled: Whether or not the public data endpoint is enabled.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] restore_point_in_time: Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: Managed instance SKU. Allowed values for sku.name: GP_Gen4, GP_Gen5, BC_Gen4, BC_Gen5
        :param pulumi.Input[str] source_managed_instance_id: The resource identifier of the source managed instance associated with create operation of this instance.
        :param pulumi.Input[int] storage_size_in_gb: Storage size in GB. Minimum value: 32. Maximum value: 8192. Increments of 32 GB allowed only.
        :param pulumi.Input[str] subnet_id: Subnet resource ID for the managed instance.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] timezone_id: Id of the timezone. Allowed values are timezones supported by Windows.
               Windows keeps details on supported timezones, including the id, in registry under
               KEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Time Zones.
               You can get those registry values via SQL Server by querying SELECT name AS timezone_id FROM sys.time_zone_info.
               List of Ids can also be obtained by executing [System.TimeZoneInfo]::GetSystemTimeZones() in PowerShell.
               An example of valid timezone id is "Pacific Standard Time" or "W. Europe Standard Time".
        :param pulumi.Input[int] v_cores: The number of vCores. Allowed values: 8, 16, 24, 32, 40, 64, 80.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagedInstanceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An Azure SQL managed instance.

        :param str resource_name: The name of the resource.
        :param ManagedInstanceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedInstanceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 administrator_login: Optional[pulumi.Input[str]] = None,
                 administrator_login_password: Optional[pulumi.Input[str]] = None,
                 collation: Optional[pulumi.Input[str]] = None,
                 dns_zone_partner: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ResourceIdentityArgs']]] = None,
                 instance_pool_id: Optional[pulumi.Input[str]] = None,
                 license_type: Optional[pulumi.Input[Union[str, 'ManagedInstanceLicenseType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 managed_instance_create_mode: Optional[pulumi.Input[Union[str, 'ManagedServerCreateMode']]] = None,
                 managed_instance_name: Optional[pulumi.Input[str]] = None,
                 minimal_tls_version: Optional[pulumi.Input[str]] = None,
                 proxy_override: Optional[pulumi.Input[Union[str, 'ManagedInstanceProxyOverride']]] = None,
                 public_data_endpoint_enabled: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 restore_point_in_time: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 source_managed_instance_id: Optional[pulumi.Input[str]] = None,
                 storage_size_in_gb: Optional[pulumi.Input[int]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timezone_id: Optional[pulumi.Input[str]] = None,
                 v_cores: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagedInstanceArgs.__new__(ManagedInstanceArgs)

            __props__.__dict__["administrator_login"] = administrator_login
            __props__.__dict__["administrator_login_password"] = administrator_login_password
            __props__.__dict__["collation"] = collation
            __props__.__dict__["dns_zone_partner"] = dns_zone_partner
            __props__.__dict__["identity"] = identity
            __props__.__dict__["instance_pool_id"] = instance_pool_id
            __props__.__dict__["license_type"] = license_type
            __props__.__dict__["location"] = location
            __props__.__dict__["maintenance_configuration_id"] = maintenance_configuration_id
            __props__.__dict__["managed_instance_create_mode"] = managed_instance_create_mode
            __props__.__dict__["managed_instance_name"] = managed_instance_name
            __props__.__dict__["minimal_tls_version"] = minimal_tls_version
            __props__.__dict__["proxy_override"] = proxy_override
            __props__.__dict__["public_data_endpoint_enabled"] = public_data_endpoint_enabled
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["restore_point_in_time"] = restore_point_in_time
            __props__.__dict__["sku"] = sku
            __props__.__dict__["source_managed_instance_id"] = source_managed_instance_id
            __props__.__dict__["storage_size_in_gb"] = storage_size_in_gb
            __props__.__dict__["subnet_id"] = subnet_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["timezone_id"] = timezone_id
            __props__.__dict__["v_cores"] = v_cores
            __props__.__dict__["dns_zone"] = None
            __props__.__dict__["fully_qualified_domain_name"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:sql:ManagedInstance"), pulumi.Alias(type_="azure-native:sql/v20180601preview:ManagedInstance"), pulumi.Alias(type_="azure-native:sql/v20200202preview:ManagedInstance"), pulumi.Alias(type_="azure-native:sql/v20200801preview:ManagedInstance"), pulumi.Alias(type_="azure-native:sql/v20201101preview:ManagedInstance"), pulumi.Alias(type_="azure-native:sql/v20210201preview:ManagedInstance"), pulumi.Alias(type_="azure-native:sql/v20210501preview:ManagedInstance")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagedInstance, __self__).__init__(
            'azure-native:sql/v20150501preview:ManagedInstance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ManagedInstance':
        """
        Get an existing ManagedInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ManagedInstanceArgs.__new__(ManagedInstanceArgs)

        __props__.__dict__["administrator_login"] = None
        __props__.__dict__["collation"] = None
        __props__.__dict__["dns_zone"] = None
        __props__.__dict__["fully_qualified_domain_name"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["instance_pool_id"] = None
        __props__.__dict__["license_type"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["maintenance_configuration_id"] = None
        __props__.__dict__["minimal_tls_version"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["proxy_override"] = None
        __props__.__dict__["public_data_endpoint_enabled"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["storage_size_in_gb"] = None
        __props__.__dict__["subnet_id"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["timezone_id"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["v_cores"] = None
        return ManagedInstance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="administratorLogin")
    def administrator_login(self) -> pulumi.Output[Optional[str]]:
        """
        Administrator username for the managed instance. Can only be specified when the managed instance is being created (and is required for creation).
        """
        return pulumi.get(self, "administrator_login")

    @property
    @pulumi.getter
    def collation(self) -> pulumi.Output[Optional[str]]:
        """
        Collation of the managed instance.
        """
        return pulumi.get(self, "collation")

    @property
    @pulumi.getter(name="dnsZone")
    def dns_zone(self) -> pulumi.Output[str]:
        """
        The Dns Zone that the managed instance is in.
        """
        return pulumi.get(self, "dns_zone")

    @property
    @pulumi.getter(name="fullyQualifiedDomainName")
    def fully_qualified_domain_name(self) -> pulumi.Output[str]:
        """
        The fully qualified domain name of the managed instance.
        """
        return pulumi.get(self, "fully_qualified_domain_name")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ResourceIdentityResponse']]:
        """
        The Azure Active Directory identity of the managed instance.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="instancePoolId")
    def instance_pool_id(self) -> pulumi.Output[Optional[str]]:
        """
        The Id of the instance pool this managed server belongs to.
        """
        return pulumi.get(self, "instance_pool_id")

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> pulumi.Output[Optional[str]]:
        """
        The license type. Possible values are 'LicenseIncluded' (regular price inclusive of a new SQL license) and 'BasePrice' (discounted AHB price for bringing your own SQL licenses).
        """
        return pulumi.get(self, "license_type")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies maintenance configuration id to apply to this managed instance.
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @property
    @pulumi.getter(name="minimalTlsVersion")
    def minimal_tls_version(self) -> pulumi.Output[Optional[str]]:
        """
        Minimal TLS version. Allowed values: 'None', '1.0', '1.1', '1.2'
        """
        return pulumi.get(self, "minimal_tls_version")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="proxyOverride")
    def proxy_override(self) -> pulumi.Output[Optional[str]]:
        """
        Connection type used for connecting to the instance.
        """
        return pulumi.get(self, "proxy_override")

    @property
    @pulumi.getter(name="publicDataEndpointEnabled")
    def public_data_endpoint_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether or not the public data endpoint is enabled.
        """
        return pulumi.get(self, "public_data_endpoint_enabled")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        Managed instance SKU. Allowed values for sku.name: GP_Gen4, GP_Gen5, BC_Gen4, BC_Gen5
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the managed instance.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="storageSizeInGB")
    def storage_size_in_gb(self) -> pulumi.Output[Optional[int]]:
        """
        Storage size in GB. Minimum value: 32. Maximum value: 8192. Increments of 32 GB allowed only.
        """
        return pulumi.get(self, "storage_size_in_gb")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Output[Optional[str]]:
        """
        Subnet resource ID for the managed instance.
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timezoneId")
    def timezone_id(self) -> pulumi.Output[Optional[str]]:
        """
        Id of the timezone. Allowed values are timezones supported by Windows.
        Windows keeps details on supported timezones, including the id, in registry under
        KEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Time Zones.
        You can get those registry values via SQL Server by querying SELECT name AS timezone_id FROM sys.time_zone_info.
        List of Ids can also be obtained by executing [System.TimeZoneInfo]::GetSystemTimeZones() in PowerShell.
        An example of valid timezone id is "Pacific Standard Time" or "W. Europe Standard Time".
        """
        return pulumi.get(self, "timezone_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vCores")
    def v_cores(self) -> pulumi.Output[Optional[int]]:
        """
        The number of vCores. Allowed values: 8, 16, 24, 32, 40, 64, 80.
        """
        return pulumi.get(self, "v_cores")

