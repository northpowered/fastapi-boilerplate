# Intro

This project was created as a template for FastAPI applications.
## What`s in the box?

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

## Installation

We`re strongly reccomend to use [Poetry](https://python-poetry.org/)

Create new virtual environment or enter to an existing one

>poetry shell

Install all dependencies from *pyproject.toml*

>poetry install

Run your app

>python3 main.py run