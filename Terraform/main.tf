//resource group: GenAI360
resource "azurerm_resource_group" "rg-tf-prod-genai360" {
    name = "rg-mzc-prod-genai360"
    location = "East US"
}
//resource group: network resource
resource "azurerm_resource_group" "rg-tf-prod-nwk" {
    name = "rg-mzc-prod-nwk"
    location = "East US"
}
//Virtual Network for network resource
resource "azurerm_virtual_network" "vnet-tf-prod-genai360" {
    name = "vnet-mzc-prod-genai360"
    location = azurerm_resource_group.rg-tf-prod-nwk.location
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    address_space = ["10.100.0.0/16"]
}
//VPN Gateway Subnet
resource "azurerm_subnet" "snet-tf-prod-vpn" {
    name = "GatewaySubnet"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    virtual_network_name = azurerm_virtual_network.vnet-tf-prod-genai360.name
    address_prefixes = ["10.100.0.0/24"]
}
//Application Gateway Subnet
resource "azurerm_subnet" "snet-tf-prod-agw" {
    name = "snet-mzc-prod-agw"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    virtual_network_name = azurerm_virtual_network.vnet-tf-prod-genai360.name
    address_prefixes = ["10.100.1.0/24"]
}
//Virtual Machine Subnet
resource "azurerm_subnet" "snet-tf-prod-vm" {
    name = "snet-mzc-prod-vm"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    virtual_network_name = azurerm_virtual_network.vnet-tf-prod-genai360.name
    address_prefixes = ["10.100.2.0/29"]
}
//Bastion Subnet
resource "azurerm_subnet" "snet-tf-prod-bastion" {
    name = "snet-mzc-prod-bastion"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    virtual_network_name = azurerm_virtual_network.vnet-tf-prod-genai360.name
    address_prefixes = ["10.100.2.8/29"]
}
//Subnet for Private Endpoints
resource "azurerm_subnet" "snet-tf-prod-pep" {
    name = "snet-mzc-prod-pep"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    virtual_network_name = azurerm_virtual_network.vnet-tf-prod-genai360.name
    address_prefixes = ["10.100.2.16/28"]
}
//Subnet for Self-hosted Integration Runtime
resource "azurerm_subnet" "snet-tf-prod-shir" {
    name = "snet-mzc-prod-shir"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    virtual_network_name = azurerm_virtual_network.vnet-tf-prod-genai360.name
    address_prefixes = ["10.100.2.32/29"]
}
//Subnet for MySQL Flexible Server
resource "azurerm_subnet" "snet-tf-prod-sql" {
    name = "snet-mzc-prod-sql"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    virtual_network_name = azurerm_virtual_network.vnet-tf-prod-genai360.name
    address_prefixes = ["10.100.3.0/24"]
    service_endpoints = ["Microsoft.Storage"]
    delegation {
        name = "fs"
        service_delegation {
            name = "Microsoft.DBforMySQL/flexibleServers"
            actions = [
                "Microsoft.Network/virtualNetworks/subnets/join/action",
            ]
        }
    }
}
//Private DNS Zones of MySQL Flexible Server
resource "azurerm_private_dns_zone" "sqltf-prod" {
    name = "sqlmzc.mysql.database.azure.com"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
}
//Virtual Network Link of Private DNS Zones
resource "azurerm_private_dns_zone_virtual_network_link" "nwk-to-sql" {
    name = "nwk-to-sql"
    private_dns_zone_name = azurerm_private_dns_zone.sqltf-prod.name
    virtual_network_id = azurerm_virtual_network.vnet-tf-prod-genai360.id
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name

    depends_on = [ azurerm_subnet.snet-tf-prod-sql ]
}

//Deploy mySQL Flexible Server
/*resource "azurerm_mysql_flexible_server" "sql-tf-prod-rds-01" {
    name = "sql-mzc-prod-rds-01"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    location = azurerm_resource_group.rg-tf-prod-nwk.location
    administrator_login = "azureuser"
    administrator_password = "Aprkwhs123!!"
    backup_retention_days = 7
    delegated_subnet_id = azurerm_subnet.snet-tf-prod-sql.id
    private_dns_zone_id = azurerm_private_dns_zone.sqltf-prod.id
    sku_name = "GP_Standard_D2ds_v4"
    version = "8.0.21"
    high_availability {
      mode = "SameZone"
    }
    maintenance_window {
      day_of_week = 0
      start_hour = 8
      start_minute = 0
    }
    storage {
        iops = 360
        size_gb = 20
    }

    depends_on = [ azurerm_private_dns_zone_virtual_network_link.nwk-to-sql ]
}*/

//Deploy CosmosDB MongoDB vCore VectorStore
resource "azurerm_resource_group_template_deployment" "terraform-arm" {
    name = "terraform-arm-01"
    resource_group_name = azurerm_resource_group.rg-tf-prod-genai360.name
    deployment_mode = "Incremental"
    template_content = file("template.json")
}

//Deploy Blob Storage
resource "azurerm_storage_account" "st-mzc-tf-extract-01" {
    name = "stmzcprodextract01"
    resource_group_name = azurerm_resource_group.rg-tf-prod-genai360.name
    location = azurerm_resource_group.rg-tf-prod-genai360.location
    account_tier = "Standard"
    account_replication_type = "LRS"
    tags = {
        environment ="Prod"
    }
}

//Private Endpoint for Blob Storage
resource "azurerm_private_endpoint" "pep-tf-prod-st-01" {
    name = "pep-mzc-prod-extract-01"
    location = azurerm_resource_group.rg-tf-prod-nwk.location
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    subnet_id = azurerm_subnet.snet-tf-prod-pep.id

    private_service_connection {
      name = "privateservice-connection"
      private_connection_resource_id = azurerm_storage_account.st-mzc-tf-extract-01.id
      subresource_names = ["blob"]
      is_manual_connection = false
    }
    private_dns_zone_group {
      name = "dns-zone-group"
      private_dns_zone_ids = [azurerm_private_dns_zone.sttf-prod.id]
    }
}
//Private DNS Zones for Blob Storage
resource "azurerm_private_dns_zone" "sttf-prod" {
    name = "privatelink.blob.core.windows.net"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
}
//Virtual Network Link for Blob Storage
resource "azurerm_private_dns_zone_virtual_network_link" "nwk-to-st" {
  name = "nwk-to-st"
  resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
  private_dns_zone_name = azurerm_private_dns_zone.sttf-prod.name
  virtual_network_id = azurerm_virtual_network.vnet-tf-prod-genai360.id
}
//Deploy Azure AI Search
resource "azurerm_search_service" "search-mzc-prod-opensearch-01" {
    name = "search-mzc-prod-search-01"
    resource_group_name = azurerm_resource_group.rg-tf-prod-genai360.name
    location = azurerm_resource_group.rg-tf-prod-genai360.location
    sku = "standard"
}
//Private Endpoint for Azure AI Search
resource "azurerm_private_endpoint" "pep-tf-prod-search-01" {
    name = "pep-mzc-prod-search-01"
    location = azurerm_resource_group.rg-tf-prod-nwk.location
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    subnet_id = azurerm_subnet.snet-tf-prod-pep.id

    private_service_connection {
      name = "privateservice-connection"
      private_connection_resource_id = azurerm_search_service.search-mzc-prod-opensearch-01.id
      subresource_names = ["searchService"]
      is_manual_connection = false
    }
    private_dns_zone_group {
      name = "dns-zone"
      private_dns_zone_ids = [azurerm_private_dns_zone.searchtf-prod.id]
    }
}
//Private DNS Zones for Azure AI Search
resource "azurerm_private_dns_zone" "searchtf-prod" {
    name = "privatelink.search.windows.net"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
}
//Virtual Network Link for Azure AI Search
resource "azurerm_private_dns_zone_virtual_network_link" "nwk-to-search" {
    name = "nwk-to-search"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    private_dns_zone_name = azurerm_private_dns_zone.searchtf-prod.name
    virtual_network_id = azurerm_virtual_network.vnet-tf-prod-genai360.id
}
//Deploy Azure OpenAI
resource "azurerm_cognitive_account" "openai-tf-prod-llm-01" {
    name = "openai-mzc-prod-llm-01"
    location = azurerm_resource_group.rg-tf-prod-genai360.location
    resource_group_name = azurerm_resource_group.rg-tf-prod-genai360.name
    kind = "OpenAI"
    sku_name = "S0"
}
/*
//Private Endpoint for Azure OpenAI
resource "azurerm_private_endpoint" "pep-tf-prod-openai-01" {
    name = "pep-mzc-prod-openai-01"
    location = azurerm_resource_group.rg-tf-prod-nwk.location
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    subnet_id = azurerm_subnet.snet-tf-prod-pep.id

    private_service_connection {
      name = "privateservice-connection"
      private_connection_resource_id = azurerm_cognitive_account.openai-tf-prod-llm-01.id
      subresource_names = ["account"]
      is_manual_connection = false
    }
    private_dns_zone_group {
      name = "dns-zone"
      private_dns_zone_ids = [azurerm_private_dns_zone.openaitf-prod.id]
    }
}
//Private DNS Zones for Azure OpenAI
resource "azurerm_private_dns_zone" "openaitf-prod" {
    name = "privatelink.openai.azure.com"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
}
//Virtual Network Link for Azure OpenAI
resource "azurerm_private_dns_zone_virtual_network_link" "nwk-to-openai" {
    name = "nwk-to-openai"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    private_dns_zone_name = azurerm_private_dns_zone.openaitf-prod.name
    virtual_network_id = azurerm_virtual_network.vnet-tf-prod-genai360.id
}*/

//Deploy Data Factory
resource "azurerm_data_factory" "adf-tf-prod-etl-01" {
    name = "adf-mzc-prod-etl-01"
    location = azurerm_resource_group.rg-tf-prod-genai360.location
    resource_group_name = azurerm_resource_group.rg-tf-prod-genai360.name
}
//Private Endpoint for Azure Data Factory
resource "azurerm_private_endpoint" "adf-tf-prod-etl-01" {
    name = "pep-mzc-prod-etl-01"
    location = azurerm_resource_group.rg-tf-prod-nwk.location
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    subnet_id = azurerm_subnet.snet-tf-prod-pep.id

    private_service_connection {
        name = "privateservice-connection"
        private_connection_resource_id = azurerm_data_factory.adf-tf-prod-etl-01.id
        subresource_names = ["dataFactory"]
        is_manual_connection = false
    }
    private_dns_zone_group {
      name = "dns-zone"
      private_dns_zone_ids = [azurerm_private_dns_zone.adftf-prod.id]
    }
}
//Private DNS Zones for Azure Data Factory
resource "azurerm_private_dns_zone" "adftf-prod" {
    name = "privatelink.datafactory.azure.net"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
}
//Virtual Network Link for Azure Data Factory
resource "azurerm_private_dns_zone_virtual_network_link" "nwk-to-adf" {
    name = "nwk-to-adf"
    resource_group_name = azurerm_resource_group.rg-tf-prod-nwk.name
    private_dns_zone_name = azurerm_private_dns_zone.adftf-prod.name
    virtual_network_id = azurerm_virtual_network.vnet-tf-prod-genai360.id
}