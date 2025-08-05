# To build image for your ApiLogicProject, see build_image.sh
#    $ sh devops/docker-image/build_image.sh .

# consider adding your version here

# ensure platform for common amd deployment, even if running on M1/2 mac --platform=linux/amd64
FROM --platform=linux/amd64 apilogicserver/api_logic_server
# FROM apilogicserver/api_logic_server  

USER root


# Install build and ODBC driver dependencies
RUN apt-get update && \
    apt-get install -y curl gnupg apt-transport-https && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev gcc g++ python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pyodbc
RUN pip install --upgrade pip && \
    pip install pyodbc==5.2.0
    
# user api_logic_server comes from apilogicserver/api_logic_server
WORKDIR /home/api_logic_project
# USER api_logic_server
COPY ../../ .

# enables docker to write into container, for sqlite
RUN chown -R api_logic_server /home/api_logic_project

CMD [ "python", "./api_logic_server_run.py" ]