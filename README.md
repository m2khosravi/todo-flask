# Todo Flask Application

This is a simple Todo application built with Flask and deployed on Azure.

## Features

- Health check endpoint
- Create new todo items
- Retrieve todo items by ID

## Setup and Deployment

### Prerequisites

- Azure account
- GitHub account
- Terraform installed locally
- Azure CLI installed locally

### Local Development

1. Clone the repository:

```
git clone https://github.com/m2khosravi/todo-flask.git
cd todo-flask
```

2. Set up a virtual environment:


```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```
4. Set up local PostgreSQL database and set the `DATABASE_URL` environment variable:

```
export DATABASE_URL=postgresql://username:password@localhost/dbname
```
5. Run database migrations:

```
flask db upgrade
```
6. Run the application:

```
flask run
```

### Deployment to Azure
1. Login to Azure CLI:

```
az login
```
2. Initialize Terraform:

```
terraform init
```
3. Apply Terraform configuration:
```
terraform apply
```
4. Set up GitHub Secrets:
- `AZURE_WEBAPP_PUBLISH_PROFILE`: Get this from the Azure portal for your App Service
- `DATABASE_URL`: The connection string to your Azure PostgreSQL database

## API Endpoints

- `GET /health`: Health check endpoint
- `GET /todos/{id}`: Get a specific todo
- `POST /todos`: Create a new todo




