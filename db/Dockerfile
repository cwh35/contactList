# Use the official PostgreSQL image from Docker Hub
FROM postgres:16-alpine

# Copy the initialization script into the container
COPY init.sql /docker-entrypoint-initdb.d/
