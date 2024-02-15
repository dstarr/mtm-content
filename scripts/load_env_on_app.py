from azure.mgmt.web import WebSiteManagementClient
from azure.identity import DefaultAzureCredential
import os

# Provide your resource group and web app name
resource_group = "ds-mtam"
webapp_name = "mtam-admin"

# Create an Azure credential object using the DefaultAzureCredential class
credential = DefaultAzureCredential()

# Create a client object for the WebSiteManagementClient class
client = WebSiteManagementClient(credential, "<your_azure_subscription_id>")

# Read the .env file and set the environment variables
with open('../.env', 'r') as file:
    for line in file:
        if not line.startswith('#'):  # Skip lines starting with #
            var = line.strip().split('=')
            if len(var) == 2:
                # Create a dictionary for the new setting
                new_setting = {var[0]: var[1]}

                # Get the current app settings
                app_settings = client.web_apps.list_application_settings(resource_group, webapp_name)

                # Update the app settings with the new setting
                app_settings.properties.update(new_setting)
                client.web_apps.update_application_settings(resource_group, webapp_name, app_settings)