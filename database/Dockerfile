# Specify the Parent Image from which we are building
FROM mysql:latest


# Set workspace
WORKDIR /services/db

# Copy app modules
COPY initial_script.sql /tmp

# Default executable of a Docker image
CMD [ "mysqld", "--init-file=/tmp/initial_script.sql" ]