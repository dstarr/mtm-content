#!/bin/bash

# Provide your resource group and web app name
resource_group="ds-mtam"
webapp_name="mtam-admin"

# Read the .env file and set the environment variables
while read -r line || [[ -n "$line" ]]; do
    if [[ ! $line == \#* ]]; then   # Skip lines starting with #
        IFS='=' read -ra VAR <<< "$line"
        az webapp config appsettings set --resource-group $resource_group --name $webapp_name --settings "${VAR[0]}=${VAR[1]}"
    fi
done <  ../.env