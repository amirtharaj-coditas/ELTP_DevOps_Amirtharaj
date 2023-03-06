from modules.virtual_machine.vm import create_vm
from modules.database.db import create_mysqldb
# runner file
# function to get user values of parameters from parameter.dev file
def get_parameter(filename, required_parameter):
    with open(filename, 'r') as file:
        for line in file:
            words = line.split()
            try:
                index = words.index(required_parameter)
            except ValueError:
                # search word not found in this line, try the next line
                continue
            #  return the next word
            return words[index + 1]
    # search word not found in file
    return None

# # Create Virtual Machine
# subscription_id = get_parameter("parameter.dev",'subscription_id')
# RESOURCE_GROUP_NAME = get_parameter("parameter.dev",'RESOURCE_GROUP_NAME')
# LOCATION = get_parameter("parameter.dev",'LOCATION')
# VNET_NAME = get_parameter("parameter.dev",'VNET_NAME')
# SUBNET_NAME = get_parameter("parameter.dev",'SUBNET_NAME')
# IP_NAME = get_parameter("parameter.dev",'IP_NAME')
# IP_CONFIG_NAME = get_parameter("parameter.dev",'IP_CONFIG_NAME')
# NIC_NAME = get_parameter("parameter.dev",'NIC_NAME')
# address_space = get_parameter("parameter.dev",'address_space')
# sub_address_prefix = get_parameter("parameter.dev",'sub_address_prefix')
# ip_sku = get_parameter("parameter.dev",'ip_sku')
# public_ip_allocation_method = get_parameter("parameter.dev",'public_ip_allocation_method')
# public_ip_address_version = get_parameter("parameter.dev",'public_ip_address_version')
# VM_NAME = get_parameter("parameter.dev",'VM_NAME')
# VM_USERNAME = get_parameter("parameter.dev",'VM_USERNAME')
# VM_PASSWORD = get_parameter("parameter.dev",'VM_PASSWORD')
# vm_publisher = get_parameter("parameter.dev",'vm_publisher')
# vm_offer = get_parameter("parameter.dev",'vm_offer')
# vm_sku = get_parameter("parameter.dev",'vm_sku' )
# vm_version = get_parameter("parameter.dev",'vm_version')
# vm_size = get_parameter("parameter.dev",'vm_size')


# # Create VM
# create_vm(subscription_id,
#               RESOURCE_GROUP_NAME,
#               LOCATION,
#               VNET_NAME,
#               SUBNET_NAME,
#               IP_NAME,
#               IP_CONFIG_NAME,
#               NIC_NAME,
#               address_space,
#               sub_address_prefix,
#               ip_sku,
#               public_ip_allocation_method,
#               public_ip_address_version,
#               VM_NAME,
#               VM_USERNAME,
#               VM_PASSWORD,
#               vm_publisher,
#               vm_offer,
#               vm_sku,
#               vm_version,
#               vm_size)

#create mysqlDB
subscription_id = get_parameter("parameter.dev",'subscription_id')
RESOURCE_GROUP_NAME = get_parameter("parameter.dev",'RESOURCE_GROUP_NAME')
SERVER_NAME = get_parameter("parameter.dev",'sqlSERVER_NAME')
LOCATION = get_parameter("parameter.dev",'sqlLOCATION')
USERNAME = get_parameter("parameter.dev",'sqlUSERNAME')
PASSWORD = get_parameter("parameter.dev",'sqlPASSWORD')
STORAGE_MB = get_parameter("parameter.dev",'sqlSTORAGE_MB')
skuname = get_parameter("parameter.dev",'skuname')
tier = get_parameter("parameter.dev",'tier')
family = get_parameter("parameter.dev",'family')
dbname = get_parameter("parameter.dev", 'dbname')

create_mysqldb(subscription_id, RESOURCE_GROUP_NAME, SERVER_NAME, LOCATION, USERNAME, PASSWORD, STORAGE_MB, skuname, tier, family, dbname)
