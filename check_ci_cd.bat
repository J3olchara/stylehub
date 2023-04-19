@echo on
chcp 1252

title Yandex codestyle checker
echo 'codestyle proceed'

venv\scripts\python.exe -m isort .
venv\scripts\python.exe -m black .
venv\scripts\python.exe -m mypy .
venv\scripts\python.exe -m flake8 .
venv\scripts\python.exe -m pylint .

cd stylehub
..\venv\scripts\python.exe manage.py makemigrations
..\venv\scripts\python.exe manage.py migrate
..\venv\scripts\python.exe manage.py test

pause
