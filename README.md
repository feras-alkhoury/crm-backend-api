# CRM Backend API

A RESTful backend API for a Customer Relationship Management (CRM) system, built with FastAPI, PostgreSQL, SQLAlchemy, and Docker.

The project demonstrates backend development skills through JWT authentication, secure password hashing, customer management, database integration, automated testing, and containerized deployment.

## Features

- JWT Authentication — Register users and log in to receive access tokens.

- Password Hashing — Store passwords as bcrypt hashes rather than plaintext.

- Customer Management — Create, retrieve, update, and delete customer records.

- Customer Search — Search customers by name, email, or company.

- Pagination — Retrieve customer records in manageable pages.

- Input Validation — Validate incoming request data using Pydantic.

- Database Integration — Use PostgreSQL with SQLAlchemy ORM.

- Automated Testing — Test API endpoints and authentication behavior with pytest.

- Docker Support — Run the API and database using Docker Compose.

- Interactive API Documentation — Explore and test endpoints through Swagger UI.

## Tech Stack

Technology

Purpose

Python

Backend programming language

FastAPI

REST API framework

PostgreSQL

Relational database

SQLAlchemy

Database ORM

Pydantic

Request and response validation

JWT

Token-based authentication

bcrypt

Password hashing

pytest

Automated testing

Docker

Application containerization

Docker Compose

Local multi-container environment

Git & GitHub

Version control and source hosting

## Architecture

The application follows a straightforward backend architecture:

Clients send HTTP requests to the FastAPI application.

FastAPI validates incoming data and handles authentication.

SQLAlchemy communicates with PostgreSQL.

The API returns structured JSON responses.

Docker Compose manages the API and database containers.

## Getting Started

Prerequisites

Docker

Docker Compose

Git

1. Clone the repository

git clone git@github.com:feras-alkhoury/crm-backend-api.git

cd crm-backend-api

2. Configure environment variables

Create a .env file in the project root.

POSTGRES_DB=crm_db

POSTGRES_USER=crm_user

POSTGRES_PASSWORD=replace_with_a_strong_password

DATABASE_URL=postgresql://crm_user:replace_with_a_strong_password@localhost:5432/crm_db

SECRET_KEY=replace_with_a_long_random_secret

Use the same database name, username, and password consistently. The password in DATABASE_URL must match POSTGRES_PASSWORD.

Security: Never commit .env or real credentials to GitHub. Use strong, unique values for your own environment.

3. Start the application

docker compose up -d --build

Check the containers:

docker compose ps

4. Verify the API

Health check:

curl http://localhost:8000/health

Open the interactive API documentation in your browser:

http://localhost:8000/docs

5. Stop the application

docker compose down

To remove the database volume and its stored data as well, use:

docker compose down -v

Warning: Removing the volume deletes the database data stored in it.

## API Endpoints

General

Method

Endpoint

Description

Authentication

GET

/

Welcome endpoint

Not required

GET

/health

Health check

Not required

Authentication

Method

Endpoint

Description

Authentication

POST

/auth/register

Register a user

Not required

POST

/auth/login

Log in and obtain a JWT

Not required

Registration accepts a JSON body:

{

  "username": "demo_user",

  "password": "StrongPassword123!"

}

Login accepts form fields named username and password.

A successful login returns an access token:

{

  "access_token": "your_access_token",

  "token_type": "bearer"

}

Use this token to access protected customer endpoints by sending the following HTTP header:

Authorization: Bearer YOUR_ACCESS_TOKEN

Customers

All customer endpoints require authentication.

Method

Endpoint

Description

POST

/customers

Create a customer

GET

/customers

List customers

GET

/customers/{customer_id}

Retrieve a customer

PUT

/customers/{customer_id}

Update a customer

DELETE

/customers/{customer_id}

Delete a customer

Customer Search and Pagination

The customer listing endpoint supports search and pagination.

Examples:

GET /customers?search=acme

GET /customers?skip=0&limit=10

GET /customers?search=example.com&skip=0&limit=5

Search supports customer names, email addresses, and company names.

Example Customer Request

{

  "name": "Alex Morgan",

  "email": "alex@example.com",

  "phone": "+1234567890",

  "company": "Example Corporation"

}

The API validates customer data and returns the created customer, including its database-generated ID.

## Database Models

User

Stores authentication information:

- id — Primary key

- username — Unique username

- hashed_password — Bcrypt password hash

Customer

Stores customer information:

- id — Primary key

- name — Customer name

- email — Unique email address

- phone — Optional phone number

- company — Optional company name

## Running Tests

Install the development dependencies in a Python virtual environment:

pip install -r requirements-dev.txt

Ensure PostgreSQL is running and your .env file is configured. Then run:

pytest -v

The test suite covers health checks, authentication, customer creation, retrieval, searching, pagination, updating, deleting, and access control.

## Project Structure

crm-backend-api/

├── app/

│   ├── main.py

│   ├── auth.py

│   ├── database.py

│   ├── models.py

│   └── schemas/

│       ├── auth.py

│       └── customer.py

├── tests/

│   └── test_api.py

├── .env.example

├── .gitignore

├── docker-compose.yml

├── Dockerfile

├── requirements.txt

├── requirements-dev.txt

└── README.md

## Future Improvements

Potential next steps include:

Database migrations with Alembic

Role-based access control

Refresh tokens and token revocation

Stronger production configuration and secret management

CI/CD with GitHub Actions

API rate limiting and additional security controls

Deployment to a cloud hosting platform

## Author

Feras Alkhoury

Information Technology Engineering student focused on backend development, REST APIs, databases, and cloud technologies.

GitHub: feras-alkhoury (https://github.com/feras-alkhoury)
