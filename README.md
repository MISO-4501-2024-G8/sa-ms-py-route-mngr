# sa-ms-py-route-mngr
Manager de Rutas

generar archivo de dependencias
```
pip3 freeze > requirements.txt
```

## Instrucciones para correr el proyecto

crear un entorno virtual
```
python3 -m venv venv
```
activar venv
```
source venv/bin/activate
```
instalar dependencias del archivo requirements.txt
```
pip3 install -r requirements.txt
```

correr flask
```
export FLASK_APP=app/app.py
export DATABASE_URL=mysql+pymysql://admin:123456789@databasesportapp.cvweuasge1pc.us-east-1.rds.amazonaws.com/db_event
flask run -p 5001
```

correr tests con pytest
```
export DATABASE_URL=
unset DATABASE_URL
pytest --cov=app/ --cov-report xml --junitxml=pytest-report.xml
coverage xml
coverage html -d coverage_report
```

Generar imagen de docker
```
docker build -t route-mngr .
```

Correr imagen de docker local
```
docker run -e DATABASE_URL=mysql+pymysql://admin:123456789@databasesportapp.cvweuasge1pc.us-east-1.rds.amazonaws.com/db_event -p 5001:5001 route-mngr

docker run -p 5001:5001 route-mngr
```