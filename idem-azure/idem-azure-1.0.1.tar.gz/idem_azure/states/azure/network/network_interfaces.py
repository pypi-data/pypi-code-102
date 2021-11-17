"""
Azure Resource Manager (ARM) Management state module.

Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0

This file implements states related to ARM network.network_interfaces.
Azure credentials must be presented via the `acct Sub`_.

TODO: Document the use of cloud_environment in the acct (yaml) data file.

.. _acct Sub: https://pypi.org/project/acct
"""
import copy

import idem_azure.helpers.exc as idemexc
from idem_azure.helpers.returns import StateReturn

# Import plugin helpers


async def present(
    hub, ctx, name, resource_group_name, network_interface_name, parameters, **kwargs
):
    """
    Ensure a network interface exists pursuant to the requested state.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param name: The name of the state (e.g., "assure vnic present").
    :param resource_group_name: Name of the resource group.
    :param network_interface_name: The name of the network interface.
    :param parameters: `NetworkInterfaces`_ parameter dictionary.
    :param kwargs: Keyward args passed direclty to the Azure SDK API.

    Example usage:
    .. code-block:: yaml
        Assure Network Interface Present:
            azure.network.network_interfaces.present:
                - resource_group_name: {{ rg_name }}
                - network_interface_name: {{ vnic_name }}
                - parameters:
                    address_prefix: "10.0.0.0/24"

    .. _NetworkInterfaces: https://docs.microsoft.com/en-us/python/api/azure-mgmt-network/azure.mgmt.network.v2020_06_01.operations.networkinterfacesoperations?view=azure-python
    """

    # Fix up any id references in parameters
    for id in parameters["ip_configurations"]:
        try:
            subkeys = id["subnet"]["id"]
            id_ret = await hub.exec.azure.utils.get_existing_id(
                ctx, hub.exec.azure.network.subnets.list, *subkeys
            )
            id["subnet"]["id"] = id_ret["ret"]
        except KeyError:
            pass  # no subnet
        try:
            subkeys = id["public_ip_address"]["id"]
            id_ret = await hub.exec.azure.utils.get_existing_id(
                ctx, hub.exec.azure.network.public_ip_addresses.list, *subkeys
            )
            id["public_ip_address"]["id"] = id_ret["ret"]
        except KeyError:
            pass  # no public ip addresses

    try:
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.network.network_interfaces.list,
            resource_group_name,
            network_interface_name,
            use_cache=True,
        )
        old = exec["ret"]
        action = "update"
        update = copy.deepcopy(old)
        update.update(parameters)
        changes = not hub.tool.azure.utils.is_within(old, parameters)
    except idemexc.NotFoundError:
        # Does not exist, create.
        old = {}
        update = parameters
        action = "create"
        changes = True

    if not changes:
        ret = StateReturn(
            name=name,
            result=True,
            comment=f"Network Interface {network_interface_name} is already present.",
        )
    elif ctx["test"]:
        ret = StateReturn(
            name=name,
            old_obj=old,
            new_obj=update,
            comment=f"Network Interface {network_interface_name} would be updated.",
        )
    else:
        exec = await hub.exec.azure.network.network_interfaces.begin_create_or_update(
            ctx, resource_group_name, network_interface_name, update, **kwargs
        )
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.network.network_interfaces.list,
            resource_group_name,
            network_interface_name,
        )
        ret = StateReturn(
            name=name,
            result=True,
            old_obj=old,
            new_obj=exec["ret"],
            comment=f"Network Interface {network_interface_name} has been {action}d.",
        )

    return ret


async def describe(hub, ctx):
    """
    Return a yaml representation of network interfaces.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`
    @return list of network interfaces in the same format as expected by the SLS file
    """
    lrg = await hub.exec.azure.utils.get_existings(
        ctx, hub.exec.azure.resource.resource_groups.list
    )

    result = {}
    for rg in lrg:
        resource_group_name = rg.get("name")
        lvnics = await hub.exec.azure.utils.get_existings(
            ctx, hub.exec.azure.network.network_interfaces.list, resource_group_name
        )

        for nic in lvnics:
            instance_id = nic.get("id")

            ip_configurations = nic.get("ip_configurations")
            for ip_config in ip_configurations:
                # Convert ids to names
                public_ip_address_id = nic["ip_configurations"][0]["public_ip_address"][
                    "id"
                ]
                public_ip_address_name = public_ip_address_id.split("/")[-1]
                subnet_id = nic["ip_configurations"][0]["subnet"]["id"]
                vnet_name = subnet_id.split("/")[-3]
                subnet_name = subnet_id.split("/")[-1]

                ip_config["public_ip_address"]["id"] = [
                    resource_group_name,
                    public_ip_address_name,
                ]
                ip_config["subnet"]["id"] = [
                    resource_group_name,
                    vnet_name,
                    subnet_name,
                ]

            parameters = {
                "location": nic.get("location"),
                "ip_configurations": ip_configurations,
                "tags": nic.get("tags"),
            }

            new_instance = [
                {"resource_group_name": resource_group_name},
                {"network_interface_name": nic.get("name")},
                {"parameters": parameters},
            ]
            result[instance_id] = {
                "azure.network.network_interfaces.present": new_instance
            }

    return result


async def absent(hub, ctx, name, resource_group_name, network_interface_name, **kwargs):
    """
    Ensure a network interface does not exist in the current subscription.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param name: The name of the state (e.g., "assure vnic absent").
    :param resource_group_name: Name of the resource group.
    :param network_interface_name: Name of the network interface.
    :param kwargs: Keyword args passed direclty to the Azure SDK API.

    Example usage:

    .. code-block: yaml

        Ensure Network Interface absent:
            azure.network.network_interfaces.absent:
              - resource_group_name: {{ rg_name }}
              - network_interface_name: {{ vnic_name }}
    """
    try:
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.network.network_interfaces.list,
            resource_group_name,
            network_interface_name,
        )
        if ctx["test"]:
            ret = StateReturn(
                name=name,
                old_obj=exec["ret"],
                new_obj={},
                comment=f"Network Interface {network_interface_name} would be deleted.",
            )
        else:
            _ = await hub.exec.azure.network.network_interfaces.begin_delete(
                ctx, resource_group_name, network_interface_name, **kwargs
            )
            ret = StateReturn(
                name=name,
                result=True,
                old_obj=exec["ret"],
                new_obj={},
                comment=f"Network Interface {network_interface_name} delete in progress.",
            )
    except idemexc.NotFoundError:
        ret = StateReturn(
            name=name,
            result=True,
            comment=f"Network Interface {network_interface_name} already absent.",
        )

    return ret
