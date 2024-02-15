from azure.mgmt.web import WebSiteManagementClient
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Provide your resource group and web app name
resource_group = "ds-mtam"
webapp_name = "mtam-admin"
env_file_path='../.env'

# Get Azure credentials
credential = DefaultAzureCredential()

# Create a client to manage resources
resource_client = ResourceManagementClient(credential, "<your_subscription_id>")

# Create a client to manage web apps
web_client = WebSiteManagementClient(credential, "<your_subscription_id>")

# Get the web app
webapp = web_client.web_apps.get(resource_group, webapp_name)

# Get the current app settings
app_settings = web_client.web_apps.list_application_settings(resource_group, webapp_name)

# Read the .env file and set the environment variables
with open(env_file_path, 'r') as file:
    for line in file:
        if not line.startswith('#'):  # Skip comments
            key, value = line.strip().split('=', 1)
            app_settings.properties[key] = value

# Update the web app with the new settings
web_client.web_apps.update_application_settings(resource_group, webapp_name, app_settings)