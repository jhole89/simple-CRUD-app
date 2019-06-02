# simple-CRUD-app
An example of a simple CRUD microservice

## Getting Started

### Prerequisites

* [Python 3.7+](https://www.python.org/downloads/)

### Installation

1. Install Python 3.7 on your Operating System as per the Python Docs.

2. Checkout the repo:
`git clone https://github.com/jhole89/simple-CRUD-app.git`

3. Setup the project dependencies:
```
$ cd simple-CRUD-app
$ export PYTHONPATH=$PYTHONPATH:$(pwd)
$ pip install -r requirements.txt
$ export FLASK_APP=crud_app.py
```

### Execution

1. From the project root run the webserver, it will be available at `localhost:5000`

```
$ flask run                           
 * Serving Flask app "crud_app.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
2. All available endpoints are listed at `'/index'`