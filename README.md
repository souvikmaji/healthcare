# Medicine Reminder

Get a reminder to take your medicine on time.
Provided with a search engine which will provide alternatives of the medicine you are lokking for with Side-effects and Symtomps

# What we are not

We are not acting as a Doctor, the data we provide will be based on History Data, we are not any consulting firm, neither we are responsible for the choices you make

# What we are

We help you to keep a Online Medical Profile
We provide a reminder for you to take the Medicine in your busy Schedule
We provide analysis on certain Factors like Possible Risks, Possible Diet charts based on your Reports.

## Setting up a development environment

We assume that you have `mysql` installed.

```bash
# Clone the code repository into ~/dev/my_app
git clone https://github.com/souvikmaji/healthcare.git

# Install required Python packages
pip install -r requirements.txt
```


# Configuring SMTP

```bash
#Copy the `local_settings_example.py` file to `local_settings.py`.
cp app/local_settings_example.py app/local_settings.py
```

Edit the `local_settings.py` file.

Specifically set all the MAIL_... settings to match your SMTP settings

Note that Google's SMTP server requires the configuration of "less secure apps".
See https://support.google.com/accounts/answer/6010255?hl=en


## Initializing the Database
```bash
# Create DB tables and populate the roles and users tables
python manage.py init_db

# Or if you have Fabric installed:
fab init_db
```


## Running the app
```bash
# Start the Flask development web server
python manage.py runserver

# Or if you have Fabric installed:
fab runserver
```

Point your web browser to http://localhost:5000/

You can make use of the following default users:
- email `user@example.com` with password `Password1`.


## Running the automated tests
```bash
# Start the Flask development web server
py.test tests/

# Or if you have Fabric installed:
fab test
```

## DB migration
