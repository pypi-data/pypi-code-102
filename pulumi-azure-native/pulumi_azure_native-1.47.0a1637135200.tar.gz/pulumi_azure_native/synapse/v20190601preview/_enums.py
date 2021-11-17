# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'CreateMode',
    'DataFlowComputeType',
    'IntegrationRuntimeEdition',
    'IntegrationRuntimeEntityReferenceType',
    'IntegrationRuntimeLicenseType',
    'IntegrationRuntimeSsisCatalogPricingTier',
    'IntegrationRuntimeType',
    'NodeSize',
    'NodeSizeFamily',
    'ResourceIdentityType',
    'SensitivityLabelRank',
    'TransparentDataEncryptionStatus',
]


class CreateMode(str, Enum):
    """
    Specifies the mode of sql pool creation.

    Default: regular sql pool creation.

    PointInTimeRestore: Creates a sql pool by restoring a point in time backup of an existing sql pool. sourceDatabaseId must be specified as the resource ID of the existing sql pool, and restorePointInTime must be specified.

    Recovery: Creates a sql pool by a geo-replicated backup. sourceDatabaseId  must be specified as the recoverableDatabaseId to restore.

    Restore: Creates a sql pool by restoring a backup of a deleted sql  pool. SourceDatabaseId should be the sql pool's original resource ID. SourceDatabaseId and sourceDatabaseDeletionDate must be specified.
    """
    DEFAULT = "Default"
    POINT_IN_TIME_RESTORE = "PointInTimeRestore"
    RECOVERY = "Recovery"
    RESTORE = "Restore"


class DataFlowComputeType(str, Enum):
    """
    Compute type of the cluster which will execute data flow job.
    """
    GENERAL = "General"
    MEMORY_OPTIMIZED = "MemoryOptimized"
    COMPUTE_OPTIMIZED = "ComputeOptimized"


class IntegrationRuntimeEdition(str, Enum):
    """
    The edition for the SSIS Integration Runtime
    """
    STANDARD = "Standard"
    ENTERPRISE = "Enterprise"


class IntegrationRuntimeEntityReferenceType(str, Enum):
    """
    The type of this referenced entity.
    """
    INTEGRATION_RUNTIME_REFERENCE = "IntegrationRuntimeReference"
    LINKED_SERVICE_REFERENCE = "LinkedServiceReference"


class IntegrationRuntimeLicenseType(str, Enum):
    """
    License type for bringing your own license scenario.
    """
    BASE_PRICE = "BasePrice"
    LICENSE_INCLUDED = "LicenseIncluded"


class IntegrationRuntimeSsisCatalogPricingTier(str, Enum):
    """
    The pricing tier for the catalog database. The valid values could be found in https://azure.microsoft.com/en-us/pricing/details/sql-database/
    """
    BASIC = "Basic"
    STANDARD = "Standard"
    PREMIUM = "Premium"
    PREMIUM_RS = "PremiumRS"


class IntegrationRuntimeType(str, Enum):
    """
    Type of integration runtime.
    """
    MANAGED = "Managed"
    SELF_HOSTED = "SelfHosted"


class NodeSize(str, Enum):
    """
    The level of compute power that each node in the Big Data pool has.
    """
    NONE = "None"
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    X_LARGE = "XLarge"
    XX_LARGE = "XXLarge"
    XXX_LARGE = "XXXLarge"


class NodeSizeFamily(str, Enum):
    """
    The kind of nodes that the Big Data pool provides.
    """
    NONE = "None"
    MEMORY_OPTIMIZED = "MemoryOptimized"


class ResourceIdentityType(str, Enum):
    """
    The type of managed identity for the workspace
    """
    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"


class SensitivityLabelRank(str, Enum):
    NONE = "None"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class TransparentDataEncryptionStatus(str, Enum):
    """
    The status of the database transparent data encryption.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"
