# Healthcare Reminder Website

## Setup
Head over to terminal and
Set database related environment variables:

```bash
export MONGODB_HOST=hostname
export MONGODB_PORT=port
export MONGODB_NAME=dbname
```

Start mongodb if it is not already running.

Set the FLASK_APP environment variable to run the application using the flask command:
```bash
export FLASK_APP=app.py
```

## Run
Run using the flask command:
```bash
flask run
```
*For other options to start the flask server in various modes take a look at the [flask manual](http://flask.pocoo.org/docs/0.12/quickstart/)*

Head over to http://127.0.0.1:5000/ to see what everything is all about.
