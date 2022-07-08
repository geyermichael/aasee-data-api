# Production Setup

## Workflow to start application

#### Start containers

```
docker compose up -d
```

#### Create database

```
docker exec -it aasee-app bash -c "python app/db/create_db.py"
```

If you run into a `No MySQL connection` error, please be patient and try again.

#### Import data in database

```
docker run --rm -it --name mysql-bash \
    -v "$PWD"/temp:/usr/src/temp \
    --network aasee-data-api_dse-network \
    --platform "linux/x86_64" mysql:5.7 \
    bash -c "mysql -h aasee-db -u root -paasee-db-password aasee_database < /usr/src/temp/dump.sql"
```

### Done!

You should now see the [api documentation](http:0.0.0.0:8000/docs).
