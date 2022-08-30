# CLI commands

## Base usage
All commands have `config` option with default value `config.toml`
Be sure about right config file when using AAA or DB  operations
```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help                          Show this message and exit.

Commands:
  aaa  Operations with users and other AAA objects
  db   Operations with DB
  run  Run application in uvicorn server with defined config file
```
## Development mode
`--reload` option invokes vanilla Uvicorl reload manager
>python3 main.py run --reload

## AAA management
### Creating superuser

**Superuser** has all available privileges, including an access to Piccolo Admin Gui and ignore all **Roles** and **Policies** restrictions

>python3 main.py aaa create superuser

### Creating user

Also you can create a simple **User** without any privileges

>python3 main.py aaa create user

### Creating JWT secret

Then you ca generate JWT secret salt, which will be stored in a place, defined in config file

>python3 main.py aaa create secret

## Database management

All database commands have an arg `application`, where you can define an app, which tables will be used. Defaults to `all`  - it means all available applications in project.

### Show DB schema
>python3 main.py db show
### Create all tables
>python3 main.py db init
### Drop all tables
>python3 main.py db drop
### Create migrations without running
>python3 main.py db mg create
### Run created migrations
>python3 main.py db mg run
