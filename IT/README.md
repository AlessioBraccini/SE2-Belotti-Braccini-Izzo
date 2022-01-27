# DREAM Application

## Backend setup
After cloning the IT repo in PyCharm:
1) Set a Python interpreter (i.e. Python 3.10), this will also create the Virtual Environment
3) Activate the environment. If the default path has been set then run:
```shell
source venv/bin/activate
```
4) Install all the project's requirements, once the `venv` is active:
```shell
pip install -r requirements.txt
```
5) Create your own `.env` file in [dream_backend](https://github.com/AlessioBraccini/SE2-Belotti-Braccini-Izzo/tree/main/IT/dream_backend) directory for environment variables. It must contains at least the following variables to correctly configure the system:
```dotenv
SECRET_KEY=your_backend_secret_key

DATABASE_NAME=your_database_name
DATABASE_USER=your_database_admin_username
DATABASE_PWD=your_database_password

LOCAL_STATIC_FILES=true/false

# if LOCAL_STATIC_FILE=false then the following variables must be set as well
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS={your_JSON_format_key_file_content_for_Google_Drive_API}
GOOGLE_DRIVE_STORAGE_SERVICE_EMAIL=your_project.iam.gserviceaccount.com
```
> _Warning_: make sure to **not** insert blank spaces and to **not** insert new lines in your JSON object for Google Drive

* `SECRET_KEY` is the key used by Django to manage authentication and hashing messages. You can set your own.
* `DATABASE_NAME`, `DATABASE_USER` and `DATABASE_PWD` are credential to access your local PostgreSQL database. If you wish to use a not local 
PostgreSQL database, you can also provide the `DATABASE_URL` variable.
* `LOCAL_STATIC_FILES` can be set either to `True` or `False` to indicate if you want to store static files locally or on Google Drive.
  * If True (or not set), then the Steering Initiatives reports uploaded to the app will be stored in 'generated/reports'
  * If False, then the reports are going to be stored on Google Drive
* `GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS` and `GOOGLE_DRIVE_STORAGE_SERVICE_MAIL` must be set if `LOCAL_STATIC_FILES=false`.
This happens because a _Google Drive API_ is going to be used to store static files. You have to: 
  * Create a _service account_ on a project in [Google Developers Console](https://developers.google.com/): this will be your service email
  * Generate a _secret service key_ a store it in a safe place. Copy and paste its content in the JSON Key variable

## Dummy Database setup

1) Create a PostgrSQL database with the following properties:
    - Name: "dream_db"
    - Owner: "dream_admin"
    - Password: "dream_pwd"
>Note: These settings are also specified in the [settings.py](https://github.com/AlessioBraccini/SE2-Belotti-Braccini-Izzo/blob/main/IT/dream_backend/settings.py) file
To do this, from terminal:
```shell
psql
postgres=\# CREATE USER dream_admin SUPERUSER WITH PASSWORD 'dream_pwd';
postgres=\# \du; #shows all the database users
postgres=\# quit; #to quit psql
```
Then from _pgAdming4_ (PostgreSQL GUI) create the "dream_db" database with "dream_admin" as owner. Alternatively, you can do this in terminal as well.
2) Add that DB to PyCharm
3) To apply changes to the tables:
```shell
python3 manage.py makemigrations
python3 manage.py migrate
```
4) Create a superuser:
```shell
python3 manage.py createsuperuser
```