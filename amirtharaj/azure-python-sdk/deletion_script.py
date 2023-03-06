from modules.virtual_machine.vm import delete_vm 
from modules.database.db import delete_mysqldb
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



# Delete VM

# subscription_id = get_parameter("parameter.dev",'subscription_id')
# RESOURCE_GROUP_NAME = get_parameter("parameter.dev",'RESOURCE_GROUP_NAME')
# VM_NAME = get_parameter("parameter.dev",'VM_NAME')

# delete_vm(subscription_id,RESOURCE_GROUP_NAME,VM_NAME)


# Delete DataBase

subscription_id = get_parameter("parameter.dev",'subscription_id')
RESOURCE_GROUP_NAME = get_parameter("parameter.dev",'RESOURCE_GROUP_NAME')
SERVER_NAME = get_parameter("parameter.dev",'sqlSERVER_NAME')

delete_mysqldb(subscription_id, RESOURCE_GROUP_NAME, SERVER_NAME)



