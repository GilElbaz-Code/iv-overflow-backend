# IVOverflow Backend

This repository contains the backend code for the IVOverflow application, a Q&A platform.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Database](#database)
- [Contributing](#contributing)
- [License](#license)

## Description

IVOverflow is a Q&A platform designed to facilitate knowledge sharing and collaboration within a community. This backend repository implements the server-side logic and database interactions for the IVOverflow application.

## Features

- User authentication and authorization
- CRUD operations for questions, answers, and user information
- Voting system for answers
- Tagging and searching for questions
- Secure communication using JWT (JSON Web Tokens)

## Prerequisites

Before running the backend, make sure you have the following prerequisites installed:

- Python 3.x
- MongoDB

## Getting Started

```bash
git clone https://github.com/GilElbaz-Code/ivoverflow-backend.git

Install dependencies:

cd ivoverflow-backend
pip install -r requirements.txt

Set up the database:

Ensure MongoDB is running on your machine.
Configure MongoDB connection in config.py.

Run the application:
python app.py
The backend server should now be running at http://localhost:5000.



