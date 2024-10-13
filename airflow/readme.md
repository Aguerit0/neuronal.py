¿QUE ES APACHE AIRFLOW?

Apache Airflow es una plataforma de código abierto para la automatización, programación y monitoreo de flujos de trabajo (workflows) en proyectos de datos. Permite crear y gestionar tareas complejas mediante la creación de DAGs (grafos acíclicos dirigidos), lo que facilita la ejecución secuencial o paralela de procesos. Airflow es ideal para coordinar tareas en pipelines de datos, como la extracción, transformación y carga (ETL), y es muy utilizado en entornos de big data y ciencia de datos.



OPERADORES

	•	Airflow ofrece varios tipos de operadores que permiten realizar diferentes tipos de tareas. Algunos de los más comunes son:
	•	PythonOperator: Ejecuta funciones Python.
	•	BashOperator: Ejecuta comandos Bash.
	•	EmailOperator: Envía correos electrónicos.
	•	MySqlOperator, PostgresOperator, etc.: Ejecuta consultas SQL en diferentes bases de datos.
	•	S3ToRedshiftOperator: Mueve datos desde Amazon S3 a Redshift.
	•	Sensor: Monitorea la disponibilidad de archivos o la finalización de una tarea.



EXECUTORS

Airflow tiene varios ejecutores que determinan cómo se ejecutan las tareas:

	•	SequentialExecutor: Ejecuta tareas secuencialmente, útil para entornos de prueba.
	•	LocalExecutor: Permite ejecutar tareas en paralelo en un solo servidor.
	•	CeleryExecutor: Utiliza un clúster distribuido para ejecutar tareas en múltiples nodos.
	•	KubernetesExecutor: Ejecuta tareas en un clúster de Kubernetes, lo que permite escalar horizontalmente.



XCOMS (Cross Communications)

	•	Intercambio de datos entre tareas: Las tareas pueden compartir información a través de XComs, una funcionalidad que permite pasar pequeños mensajes o datos entre tareas.



CONNECT PGADMIN + DOCKER
1- running docker + airflow: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html


2- add in docker.yml:
    pgadmin:
        image: dpage/pgadmin4
        environment:
            PGADMIN_DEFAULT_EMAIL: example@gmail.com
            PGADMIN_DEFAULT_PASSWORD: 9864
        ports:
        - "5050:80"
		healthcheck:
            test: ["CMD-SHELL", "pg_isready -U airflow"]
            interval: 10s
            timeout: 5s
            retries: 5


3- command:
    docker pull dpage/pgadmin4
    or install container in docker desktop


4- command:
    docker-compose config
    docker-compose up --build


5- add new server in pdadming 5050 port:
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