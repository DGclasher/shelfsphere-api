# Shelfsphere API

## Description

A simple Library Management System

#### Get the complete documentation from [here](https://raw.githubusercontent.com/DGclasher/shelfsphere-api/main/docs/library-management-system-docs-dg.pdf)

#### Frontend Client : [shelfsphere](https://dgclasher.github.io/shelfsphere/) | [repo](https://github.com/DGclasher/shelfsphere)

## Setup

On the root directory of project, run
```
python3 -m venv venv && source venv/bin/activate
```

Generate a secret key from [here](https://djecrety.ir/) and make an `.env` file
```
SECRET_KEY=< secret key >
DB_NAME=< postgresql database name >
DB_USER=< postgresql username >
DB_PASS=< password >
DB_HOST=< postgresql host >
DB_PORT=< postgresql port >
```

Install dependencies and create setup
```
make setup
```

Run the server
```
python3 manage.py runserver
```