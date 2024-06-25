provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "todo-flask-rg"
  location = "East US"
}

resource "azurerm_postgresql_server" "server" {
  name                = "todo-flask-psql-server"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku_name = "B_Gen5_1"

  storage_mb                   = 5120
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true

  administrator_login          = "psqladmin"
  administrator_login_password = var.db_password
  version                      = "11"
  ssl_enforcement_enabled      = true
}

resource "azurerm_postgresql_database" "db" {
  name                = "tododb"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_postgresql_server.server.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}

resource "azurerm_app_service_plan" "plan" {
  name                = "todo-flask-app-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "app" {
  name                = "todo-flask-app-service"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.plan.id

  site_config {
    python_version = "3.9"
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "DATABASE_URL" = "postgresql://${azurerm_postgresql_server.server.administrator_login}:${var.db_password}@${azurerm_postgresql_server.server.fqdn}:5432/${azurerm_postgresql_database.db.name}"
  }
}

variable "db_password" {
  description = "PostgreSQL server administrator password"
  type        = string
  sensitive   = true
}