@echo on
chcp 1252

title Yandex fixture loader
echo 'fixture loader proceed'

cd stylehub
..\venv\scripts\python.exe manage.py makemigrations
..\venv\scripts\python.exe manage.py migrate
cd ..
venv\scripts\python.exe manage.py loaddata fixtures\save.json

pause
