from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
import time

def create_vm(subscription_id,
              RESOURCE_GROUP_NAME,
              LOCATION,
              VNET_NAME,
              SUBNET_NAME,
              IP_NAME,
              IP_CONFIG_NAME,
              NIC_NAME,
              address_space,
              sub_address_prefix,
              ip_sku,
              public_ip_allocation_method,
              public_ip_address_version,
              VM_NAME,
              VM_USERNAME,
              VM_PASSWORD,
              vm_publisher,
              vm_offer,
              vm_sku,
              vm_version,
              vm_size):
    


    # Acquire a credential object using CLI-based authentication.
    credential = AzureCliCredential()

    # Retrieve subscription ID from environment variable.
    #subscription_id = subscription_id


    # Step 1: Provision a resource group

    # Obtain the management object for resources, using the credentials
    # from the CLI login.
    resource_client = ResourceManagementClient(credential, subscription_id)

    # Constants we need in multiple places: the resource group name and
    # the region in which we provision resources. You can change these
    # values however you want.
    #RESOURCE_GROUP_NAME = "amirth_PythonAzureExample-VM-rg"
    #LOCATION = "eastus2"

    # Provision the resource group.
    rg_result = resource_client.resource_groups.create_or_update(
        RESOURCE_GROUP_NAME, {"location": LOCATION}
    )

    print(
        f"Provisioned resource group {rg_result.name} in the \
    {rg_result.location} region"
    )

    # For details on the previous code, see Example: Provision a resource
    # group at https://learn.microsoft.com/azure/developer/python/
    # azure-sdk-example-resource-group

    # Step 2: provision a virtual network
    print("_______line 49 passed_____")
    # A virtual machine requires a network interface client (NIC). A NIC
    # requires a virtual network and subnet along with an IP address.
    # Therefore we must provision these downstream components first, then
    # provision the NIC, after which we can provision the VM.

    # Network and IP address names
    #VNET_NAME = "ami_python-example-vnet"
    #SUBNET_NAME = "ami_python-example-subnet"
    #IP_NAME = "ami_python-example-ip"
    #IP_CONFIG_NAME = "ami_python-example-ip-config"
    #NIC_NAME = "ami_python-example-nic"

    # Obtain the management object for networks
    network_client = NetworkManagementClient(credential, subscription_id)
    time.sleep(15)
    # Provision the virtual network and wait for completion
    poller = network_client.virtual_networks.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        VNET_NAME,
        {
            "location": LOCATION,
            "address_space": {"address_prefixes": [address_space]},
        },
    )
    print("___________code passed the line 74_________")

    vnet_result = poller.result()

    print(
        f"Provisioned virtual network {vnet_result.name} with address \
    prefixes {vnet_result.address_space.address_prefixes}"
    )
    print("______line 80 passed________")
    # Step 3: Provision the subnet and wait for completion
    time.sleep(15)
    poller = network_client.subnets.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        VNET_NAME,
        SUBNET_NAME,
        {"address_prefix": sub_address_prefix},
    )
    subnet_result = poller.result()

    print(
        f"Provisioned virtual subnet {subnet_result.name} with address \
    prefix {subnet_result.address_prefix}"
    )
    #time.sleep(20)
    # Step 4: Provision an IP address and wait for completion
    poller = network_client.public_ip_addresses.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        IP_NAME,
        {
            "location": LOCATION,
            "sku": {"name": ip_sku},
            "public_ip_allocation_method": public_ip_allocation_method,
            "public_ip_address_version": public_ip_address_version,
        },
    )

    ip_address_result = poller.result()

    print(
        f"Provisioned public IP address {ip_address_result.name} \
    with address {ip_address_result.ip_address}"
    )
    #time.sleep(15)
    # Step 5: Provision the network interface client
    poller = network_client.network_interfaces.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        NIC_NAME,
        {
            "location": LOCATION,
            "ip_configurations": [
                {
                    "name": IP_CONFIG_NAME,
                    "subnet": {"id": subnet_result.id},
                    "public_ip_address": {"id": ip_address_result.id},
                }
            ],
        },
    )

    nic_result = poller.result()

    print(f"Provisioned network interface client {nic_result.name}")

    # Step 6: Provision the virtual machine

    # Obtain the management object for virtual machines
    compute_client = ComputeManagementClient(credential, subscription_id)

    #VM_NAME = "vm1"
    #VM_USERNAME = "ami_azureuser"
    #VM_PASSWORD = "ChangePa$$w0rd24"

    print(
        f"Provisioning virtual machine {VM_NAME}; this operation might \
    take a few minutes."
    )

    # Provision the VM specifying only minimal arguments, which defaults
    # to an Ubuntu 18.04 VM on a Standard DS1 v2 plan with a public IP address
    # and a default virtual network/subnet.

    poller = compute_client.virtual_machines.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        VM_NAME,
        {
            "location": LOCATION,
            "storage_profile": {
                "image_reference": {
                    "publisher": vm_publisher,
                    "offer": vm_offer,
                    "sku": vm_sku,
                    "version": vm_version,
                }
            },
            "hardware_profile": {"vm_size": vm_size},
            "os_profile": {
                "computer_name": VM_NAME,
                "admin_username": VM_USERNAME,
                "admin_password": VM_PASSWORD,
            },
            "network_profile": {
                "network_interfaces": [
                    {
                        "id": nic_result.id,
                    }
                ]
            },
        },
    )

    vm_result = poller.result()
    print(f"Provisioned virtual machine {vm_result.name}")


# deletion of Virtual Machine
def delete_vm(subscription_id,resource_group_name,vm_name):

    # Create credentials object
    credential = AzureCliCredential()

    # Obtain the management object for virtual machines
    compute_client = ComputeManagementClient(credential, subscription_id)

    # Delete the virtual machine
    compute_client.virtual_machines.begin_delete(resource_group_name, vm_name).wait()
    print("Virtal machine successfully deleted")

    #TO DELETE THE DISK ASSOCIATED WITH VM
    #disk = compute_client.disks.get(RESOURCE_GROUP_NAME, DISK_NAME)
    #compute_client.disks.begin_delete(RESOURCE_GROUP_NAME, DISK_NAME).wait()
