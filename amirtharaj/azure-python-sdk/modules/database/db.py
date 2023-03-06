from azure.identity import AzureCliCredential
from azure.mgmt.rdbms.mysql import MySQLManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.rdbms.mysql.models import ServerForCreate, ServerPropertiesForDefaultCreate, ServerVersion
from azure.mgmt.rdbms import postgresql, postgresql_flexibleservers
from azure.mgmt.rdbms.mysql.models import (
    ServerForCreate,
    ServerPropertiesForDefaultCreate,
    StorageProfile,
    Sku,
    CreateMode,
)
def create_mysqldb(subscription_id, RESOURCE_GROUP_NAME, SERVER_NAME, LOCATION, USERNAME, PASSWORD, STORAGE_MB, skuname,tier, family, dbname):
    # Acquire a credential object using CLI-based authentication.
    credential = AzureCliCredential()

    resource_client = ResourceManagementClient(credential, subscription_id)
    rg_result = resource_client.resource_groups.create_or_update(
        RESOURCE_GROUP_NAME, {"location": LOCATION}
    )

    print(
        f"Provisioned resource group {rg_result.name} in the \
    {rg_result.location} region"
    )


    # Create a MySQL server object
    server = ServerForCreate(
        location=LOCATION,
        sku=Sku(name=skuname, tier=tier, family=family),
        properties=ServerPropertiesForDefaultCreate(
            create_mode=CreateMode.default,
            administrator_login=USERNAME,
            administrator_login_password=PASSWORD,
            storage_profile=StorageProfile(storage_mb=STORAGE_MB),
        ),
    )

    # Create a MySQL server client
    mysql_client = MySQLManagementClient(credential, subscription_id)

    # Create a MySQL server in Azure

    poller = mysql_client.servers.begin_create(
        RESOURCE_GROUP_NAME, SERVER_NAME, server
    )

    # Wait for the operation to complete
    server_result = poller.result()
    print(f"Created MySQL server: {server_result.fully_qualified_domain_name}")

    #creating Database
    poller = mysql_client.databases.begin_create_or_update(RESOURCE_GROUP_NAME,
        SERVER_NAME, dbname, {})
    db_result = poller.result()
    print(f"Provisioned MySQL database {db_result.name} with ID {db_result.id}")


# Delete mysql server

def delete_mysqldb(subscription_id, RESOURCE_GROUP_NAME, SERVER_NAME):

    # Acquire a credential object using CLI-based authentication.
    credential = AzureCliCredential()

    mysql_client = MySQLManagementClient(credential,subscription_id)

    mysql_client.servers.begin_delete(
    resource_group_name=RESOURCE_GROUP_NAME,
    server_name=SERVER_NAME
    ).wait()

    print("Database deleted successfully!")

