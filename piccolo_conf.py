from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine
from configuration import config

DB = PostgresEngine(config={'dsn':config.database.build_connection_string()})


# A list of paths to piccolo apps
# e.g. ['blog.piccolo_app']
APP_REGISTRY = AppRegistry(apps=["accounting.piccolo_app"])
