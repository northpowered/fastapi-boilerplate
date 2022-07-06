# FastAPI boilerplate

Work in progress!

Another [FastAPI](https://github.com/tiangolo/fastapi)
 Boilerplate with:
 - [Piccolo ORM](https://github.com/piccolo-orm/piccolo) and [Piccolo Admin](https://github.com/piccolo-orm/piccolo_admin)
 - Ready JWT authentication (including DB schema and CRUD for it)
 - Config file parcer for *.ini files, based (on standart Python configparcer and [PyDantic](https://github.com/samuelcolvin/pydantic)
 - Out-the-box [Hashicorp Vault](https://github.com/hashicorp/vault) integration, for DB credentials at first
 - Small CLI, based on [Typer](https://github.com/tiangolo/typer)
 - Out-the-box [OpenTelemetry](https://github.com/orgs/open-telemetry) collector
 - [Prometheus](https://github.com/prometheus/prometheus) endpoint


## Usage
```bash
Usage: main.py [OPTIONS] [CONFIG]

  Run application in uvicorn server with defined config file

Arguments:
  [CONFIG]  Path to config file  [default: config.ini]

Options:
  --reload / --no-reload          Allow Uvicorn watch file chang
```
### Installation:

```bash
    pip install -r requirements.txt
    python3 main.py  run
```
