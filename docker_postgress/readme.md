1- running docker + airflow: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html


2- add in docker.yml:
    pgadmin:
        image: dpage/pgadmin4
        environment:
            PGADMIN_DEFAULT_EMAIL: example@gmail.com
            PGADMIN_DEFAULT_PASSWORD: 9864
        ports:
        - "5050:80"



3- command:
    docker pull dpage/pgadmin4
    or install container in docker desktop


4- command:
    docker-compose config
    docker-compose up --build

5- add in docker.yml:
      pgadmin:
        ...
        healthcheck:
            test: ["CMD-SHELL", "pg_isready -U airflow"]
            interval: 10s
            timeout: 5s
            retries: 5

6- add new server in pdadming 5050 port:
    server name:
        "Airflow PostgreSQL"
    Host:
        postgres (name server in  docker-compose.yml)
    Puerto:
        5432 (default port PostgreSQL "in container")
    database:
        airflow (config name in docker-compose.yml)
    user:
        airflow (user name in docker-compose.yml)
    pass:
        airflow (pass in docker-compose.yml)



## CREATE AND UPDATE TABLE
1- command:
    pip install apache-airflow-providers-postgres

2- create dag

3- create connection in airflow dash (admin > connections):
    Conn Id: postgres_airflow
    Conn Type: Postgres
    Host: postgres
    Puerto: 5432
    Base de datos: airflow
    Usuario: airflow
    Contraseña: airflow


4- add in sql:
    autocommit=True
