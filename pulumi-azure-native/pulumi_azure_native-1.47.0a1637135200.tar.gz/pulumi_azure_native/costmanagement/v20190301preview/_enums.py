# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ConnectorBillingModel',
]


class ConnectorBillingModel(str, Enum):
    """
    Connector billing model
    """
    TRIAL = "trial"
    AUTO_UPGRADE = "autoUpgrade"
    PREMIUM = "premium"
    EXPIRED = "expired"
