# Data Science Ecosystems - Project

This application is part of the [Data Science Management](https://www.hnu.de/studium/studiengaenge/bachelorstudiengaenge/data-science-management-bsc) study program and the final project of the Data Science Ecosystem course.

We created a [dockerized](https://www.docker.com/) Web-API for the [Aasee](https://www.stadt-muenster.de/tourismus/sehenswertes/aasee.html) using [FastApi](https://fastapi.tiangolo.com/) and a [MySQL](https://www.mysql.com/de/) database.

One feature is the prediction of the water temperature for a future day by a given outdoor temperature on that day.

## Datasets

- [Aasee Data](https://github.com/od-ms/aasee-monitoring/tree/main)
- [Brightsky API](https://brightsky.dev/) for outdoor temperature

## Getting Started

Create your .env file. It is neccessary for the application to run.

```
cp .env.example .env
```

## Docker

We use [make](https://www.gnu.org/software/make/manual/make.html) with a makefile to simplify commands.
So if you can use `make`, perfect!

If not, follow the specific setup files.

### Production

Just run

```
make run-app
```

The API documentation can be accessed under [0.0.0.0:8000/docs](http://0.0.0.0:8000/docs).

For more information, see the [production setup](production.md).

To stop run

```
make stop-app
```

### Development

If you want to dig into the code and do further development you have to create a docker image first.

Run

```
docker build -t aasee-app-dev .
```

After that run

```
make run-app-dev
```

A uvicorn server will start.

The API documentation can be accessed under [0.0.0.0:8042/docs](http://0.0.0.0:8042/docs).

For more information, see the [development setup](development.md).

To stop the development run

```
make stop-app-dev
```

### Note

Be aware that we use `PWD` [_print working directory_](https://en.wikipedia.org/wiki/Pwd) in our docker commands.
If you run into errors due to this please make changes and use your current working directory path.

### Authors

- Andreas Geyer (Docker, make)
- Michael Geyer (MySQL, FastAPI)
- Tim Werner (Data Analytics)
