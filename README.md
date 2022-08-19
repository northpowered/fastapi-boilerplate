[![CodeFactor](https://www.codefactor.io/repository/github/northpowered/fastapi-boilerplate/badge/master)](https://www.codefactor.io/repository/github/northpowered/fastapi-boilerplate/overview/master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=northpowered_fastapi-boilerplate&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=northpowered_fastapi-boilerplate)
# FastAPI boilerplate

Work in progress, read [issues](https://github.com/northpowered/fastapi-boilerplate/issues)

Another [FastAPI](https://github.com/tiangolo/fastapi)
 Boilerplate with:
 - [Piccolo ORM](https://github.com/piccolo-orm/piccolo) and [Piccolo Admin GUI](https://github.com/piccolo-orm/piccolo_admin)
 - Ready JWT authentication (including DB schema and CRUD for it)
 - Native API versioning
 - Configfile parcer for toml and yaml files, based on [PyDantic](https://github.com/samuelcolvin/pydantic)
 - Out-the-box [Hashicorp Vault](https://github.com/hashicorp/vault) integration, for DB credentials at first
 - Small CLI, based on [Typer](https://github.com/tiangolo/typer)
 - Out-the-box [OpenTelemetry](https://github.com/orgs/open-telemetry) collector
 - [Prometheus](https://github.com/prometheus/prometheus) endpoint
 - Request ID propagation to logger, Request and Responce (addition to Headers)


## Usage
#### Base usage
```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help                          Show this message and exit.

Commands:
  aaa  Operations with users and other AAA objects
  db   Operations with DB
  run  Run application in uvicorn server with defined config file
```
#### Dev mode
```
>> python3 main.py run --reload
```
#### AAA management
```
# Create superuser with all privileges
>> python3 main.py aaa create superuser
# Create user
>> python3 main.py aaa create user
# Generating JWT secret
>> python3 main.py aaa create secret
```
#### Database management
```
# Show database schema (all or per application)
>> python3 main.py db show
# Create all tables (all or per application)
>> python3 main.py db init
# Drop all tables (all or per application)
>> python3 main.py db drop

# Migrations
# Create without running (all or per application)
>> python3 main.py db mg create
# Run created (all or per application)
>> python3 main.py db mg run
```
### Installation:

```bash
poetry shell
poetry install
python3 main.py run
```
