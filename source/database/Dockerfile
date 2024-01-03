FROM postgres:latest

# Copy the SQL dump script to the initialization directory
COPY ./init.sql /docker-entrypoint-initdb.d/
