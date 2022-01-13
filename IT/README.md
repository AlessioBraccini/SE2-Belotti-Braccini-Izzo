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