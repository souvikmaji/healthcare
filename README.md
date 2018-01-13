# Healthcare Reminder Website

## Setup
Head over to terminal and
Set database related environment variables:

```bash
export MONGODB_HOST=localhost
export MONGODB_PORT=27017
export MONGODB_NAME=healthcare
```

Set the FLASK_APP environment variable to run the application using the flask command:
```bash
export FLASK_APP=app.py
```



## Run
Run using the flask command:
```bash
flask run
```
Or alternatively use `python’s -m` switch with Flask:
```bash
python -m flask run
```
