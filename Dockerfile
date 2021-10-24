FROM ubuntu:20.04
RUN apt-get update -y && apt-get install -y python3-pip python-dev mariadb-client-core-10.3 wget curl
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup && chmod +x mariadb_repo_setup && ./mariadb_repo_setup --mariadb-server-version="mariadb-10.5"
RUN apt-get update -y && apt-get install -y libmariadb3 libmariadb-dev
RUN apt-get install -y python3-psycopg2
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
COPY ./app /app
RUN pip install -r requirements.txt
CMD [ "python3", "./main.py" ]
