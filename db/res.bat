@echo OFF

FOR /F "tokens=*" %%a IN ('python -c "import sys; sys.path.append('..'); from config import config; print(config['db']['url'])"') DO (SET db=%%a)


psql "%db%" -1 -f "./schema.sql"
psql "%db%" -1 -f "./town-coordinates.sql"
python "./set-current-tournament.py" "%db%"
psql "%db%" -1 -f "./users.sql"
python "./problems.py" "%db%"
psql "%db%" -1 -f "./assign-problems.sql"
