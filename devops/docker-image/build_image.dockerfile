# To build image for your ApiLogicProject, see build_image.sh
#    $ sh devops/docker-image/build_image.sh .

# consider adding your version here

# ensure platform for common amd deployment, even if running on M1/2 mac --platform=linux/amd64
FROM --platform=linux/amd64 apilogicserver/api_logic_server
# FROM apilogicserver/api_logic_server  

USER root

# Install system dependencies needed to build pyodbc
RUN apt-get update && \
    apt-get install -y \
        gcc \
        g++ \
        python3-dev \
        unixodbc-dev \
        curl \
        gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pyodbc version 5.2.0
RUN pip install --upgrade pip && \
    pip install pyodbc==5.2.0
    
# user api_logic_server comes from apilogicserver/api_logic_server
WORKDIR /home/api_logic_project
# USER api_logic_server
COPY ../../ .

# enables docker to write into container, for sqlite
RUN chown -R api_logic_server /home/api_logic_project

CMD [ "python", "./api_logic_server_run.py" ]