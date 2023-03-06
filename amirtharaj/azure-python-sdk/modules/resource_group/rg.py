#core logic for your module - RG
from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
import time

def create_vm(subscription_id,
              RESOURCE_GROUP_NAME,
              LOCATION)