@echo on
chcp 1252

title Yandex codestyle checker
echo 'codestyle proceed'
venv\scripts\python.exe -m isort .
venv\scripts\python.exe -m black .
venv\scripts\python.exe -m mypy .
venv\scripts\python.exe -m flake8 .
venv\scripts\python.exe -m pylint .
pause