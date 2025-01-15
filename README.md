# Project Name

Expenze

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies](#technologies)
4. [Installation](#installation)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
    - [Authentication](#authentication)
    - [Wallets](#wallets)
    - [Transactions](#transactions)
    - [User Information](#user-information)
7. [License](#license)

## Introduction

This project is a Django backend REST API with React Native mobile integration, hosted on AWS. The project includes features for managing users, wallets, transactions, and more. Users can log in, create wallets, make transactions, and view their balances via an API and React Native mobile app.

## Features

- **User Authentication**: Login and JWT-based authentication.
- **Transaction Management**: Create, view, and group transactions by day, week, or month.
- **Wallet Management**: Create and manage wallets.
- **Category Management**: Organize transactions by income/expense categories.
- **Total Balance Calculation**: View the total balance of the user.

## Technologies

- **Backend**: Django, Django REST Framework, Simple JWT, AWS
- **Frontend**: React Native, Axios, AsyncStorage
- **Database**: PostgreSQL (or your preferred database)
- **Deployment**: AWS EC2, Nginx, Gunicorn
- **Authentication**: JWT (JSON Web Tokens)

## Installation

### Backend Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Run the server:
    ```bash
    python manage.py runserver
    ```
    The backend will now be running at `http://127.0.0.1:8000/`.

### Frontend Setup

1. Install the dependencies:
    ```bash
    npm install
    ```

2. Run the app:
    ```bash
    npm start
    ```
    The frontend app should now be running on your local machine.

## Usage

- **Login**: Users can log in by providing a username and password. A JWT token will be returned on successful authentication, which can be used for subsequent API requests.
  
- **Creating Wallets**: After login, users can create and manage wallets.
  
- **Transactions**: Users can create transactions, view them, and group them by day, week, or month.

## API Endpoints

### Authentication

- **POST /api/token/**  
  Obtain JWT token for login.  
  Request body:
    ```json
    {
      "username": "user",
      "password": "password"
    }
    ```

- **POST /api/token/refresh/**  
  Refresh the JWT token using the refresh token.

### Wallets

- **GET /wallets/<str:usr>/**  
  List all wallets for a user.

- **POST /wallet/**  
  Create a new wallet for a user.

- **GET /wallet/<str:usr>/<int:pk>/**  
  Get the details of a specific wallet.

### Transactions

- **GET /transactions/<str:usr>/**  
  List all transactions for a user.

- **GET /transactions_by_day/<str:usr>/**  
  Group transactions by day.

- **GET /transactions_by_week/<str:usr>/**  
  Group transactions by week.

- **GET /transactions_by_month/<str:usr>/**  
  Group transactions by month.

### User Information

- **GET /user/total-balance/<str:usr>/**  
  Get the total balance of a user.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
