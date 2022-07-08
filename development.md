# Development Setup

## Workflow to start development

Build image from current Dockerfile

```
docker build -t aasee-app-dev .
```

Create network

```
docker network create dse-network-dev
```

Run MySQL container

```
docker run --rm --name aasee-db-dev -e MYSQL_ROOT_PASSWORD=aasee-db-password \
    -d --network dse-network-dev --platform "linux/x86_64" mysql:5.7
```

Run Python container with uvicorn application

```
docker run -e ENV=dev --name aasee-app-dev --rm -it \
    -v "$PWD":/usr/src --network dse-network-dev \
    -p 8042:8000 aasee-app-dev
```

Create database

```
docker exec -it aasee-app-dev bash -c "python app/db/create_db.py"
```

Import data in database

```
docker run --rm -it --name mysql-bash \
    -v "$PWD"/temp:/usr/src/temp \
    --network dse-network-dev \
    --platform "linux/x86_64" mysql:5.7 \
    bash -c "mysql -h aasee-db-dev -u root -paasee-db-password aasee_database < /usr/src/temp/dump.sql"
```

## Testing

For testing the api you can use a helper container.

```
docker run -e ENV=dev --name aasee-app-dev-bash --rm -it \
    -v "$PWD":/usr/src --network dse-network-dev \
    -p 8043:8000 aasee-app-dev bash
```

Now run `pytest -v`

## Use current data

The application uses the `temp/dump.sql` file to init the database data.
If you want to use the current data, you should follow these steps.

Run the development setup **without creating the database and importing the data!**

Run a helper container to open your application with bash.

```
docker run -e ENV=dev --name aasee-app-dev-bash --rm -it \
    -v "$PWD":/usr/src --network dse-network-dev \
    -p 8043:8000 aasee-app-dev bash
```

Be aware of that the next step might run for a few hours.
Run `python app/db/init_with_current_data.py` inside the helper container.

Now you can export the database via mysqldump using another helper container.

```
docker run --rm -it --name mysql-bash \
    -v "$PWD"/temp:/usr/src/temp \
    --network dse-network-dev \
    --platform "linux/x86_64" mysql:5.7 \
    bash -c "mysqldump -h aasee-db-dev -u root -paasee-db-password aasee_database > /usr/src/temp/current_data.sql"
```

At this point you can use the application with the current data.

To use your created sql file for the next time, change the import path from `/usr/src/temp/dump.sql` to `/usr/src/temp/current_data.sql` or rename the file accordingly.

## Stop development setup

Run `docker kill aasee-app-dev` and `docker kill aasee-db-dev`

## MySQL Helper Container

```
docker run -it --network dse-network-dev \
    --rm --platform "linux/x86_64" mysql:5.7 \
    mysql -h aasee-db-dev -u root -p
```
