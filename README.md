# Shelfsphere API

## Description

A simple Library Management System

## Setup

On the root directory of project, run
```
python3 -m venv venv && source venv/bin/activate
```

Generate a secret key from [here](https://djecrety.ir/) and make an `.env` file
```
SECRET_KEY=< secret key >
DB_NAME=< mysql database name >
DB_USER=< mysql username >
DB_PASS=< password >
DB_HOST=< mysql host >
DB_PORT=< mysql port >
```

Install dependencies and create setup
```
make setup
```

Run the server
```
python3 manage.py runserver
```