FROM ubuntu:20.04
RUN apt-get update -y && apt-get install -y python3-pip python-dev mariadb-client-core-10.3 wget curl
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup && chmod +x mariadb_repo_setup && ./mariadb_repo_setup --mariadb-server-version="mariadb-10.5"
RUN apt-get update -y && apt-get install -y libmariadb3 libmariadb-dev
RUN apt-get install -y python3-psycopg2
WORKDIR /app
COPY ./app /app
COPY ./app/static /app/static/
COPY ./app/templates /app/templates/
RUN pip install -r requirements.txt
RUN chmod +x /script.sh
ENTRYPOINT ["/script.sh"]
