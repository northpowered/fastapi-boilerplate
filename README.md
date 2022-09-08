[![CodeFactor](https://www.codefactor.io/repository/github/northpowered/fastapi-boilerplate/badge/master)](https://www.codefactor.io/repository/github/northpowered/fastapi-boilerplate/overview/master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=northpowered_fastapi-boilerplate&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=northpowered_fastapi-boilerplate)
[![CI](https://github.com/northpowered/fastapi-boilerplate/actions/workflows/ci.yml/badge.svg)](https://github.com/northpowered/fastapi-boilerplate/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/northpowered/fastapi-boilerplate/branch/master/graph/badge.svg?token=2E6WMLULD7)](https://codecov.io/gh/northpowered/fastapi-boilerplate)
# FastAPI boilerplate

> Version: 1.1.2

Work in progress, please read [issues](https://github.com/northpowered/fastapi-boilerplate/issues)

Full documentation is available on [Github pages](https://northpowered.github.io/fastapi-boilerplate/)

## Another [FastAPI](https://github.com/tiangolo/fastapi) Boilerplate with:
* [FastAPI](https://github.com/tiangolo/fastapi) as a base ASGI app
* [Piccolo ORM](https://github.com/piccolo-orm/piccolo) for a database operations
* [Piccolo Admin GUI](https://github.com/piccolo-orm/piccolo_admin) for a convenient database management
* [Hashicorp Vault](https://github.com/hashicorp/vault) integration for DB credentials (with auto-rotating), JWT secrets and other
* Custom `Accounting` CRUD application for managing 
  * Users
  * Roles
  * Groups
  * Permissions
  * Security policies
* JWT autehntication
* API versioning
* [PyDantic](https://github.com/samuelcolvin/pydantic)-based flexible configfile parcer (`toml` and `yaml` formats supports)
* [Typer](https://github.com/tiangolo/typer)-based CLI management
* [Prometheus](https://github.com/prometheus/prometheus) endpoint based on [Starlette exporter](https://github.com/stephenhillier/starlette_exporter)
* [OpenTelemetry](https://github.com/orgs/open-telemetry) collector
* Request ID propagation for logger, Request and Response (injection to Headers)
* CI pipeline for linting and testing (with coverage)

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
All CLI commands with descriptions are placed [here](https://northpowered.github.io/fastapi-boilerplate/cli/)

## Installation

We`re strongly reccomend to use [Poetry](https://python-poetry.org/)

Create new virtual environment or enter to an existing one

>poetry shell

Install all dependencies from *pyproject.toml*

>poetry install

Run your app

>python3 main.py run