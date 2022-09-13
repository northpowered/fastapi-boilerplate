from loguru import logger
from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine as _PostgresEngine
from configuration import config
from typing import Any, Sequence, Dict
from piccolo.querystring import QueryString
from asyncpg.exceptions import InvalidPasswordError, UndefinedTableError
from utils.events import load_vault_db_creds, reload_db_creds


# TODO asyncio warning about db auth fail, redone in _run_in_new_connection
class PostgresEngine(_PostgresEngine):
    """
    Implemetation of base PostgresEngine class of Piccolo ORM
    Added Vault integration for obtaining new DB credentials after expiration
    """

    def __init__(
        self,
        config: Dict[str, Any],
        extensions: Sequence[str] = (),
        log_queries: bool = False,
        extra_nodes: Dict[str, _PostgresEngine] = None
    ) -> None:
        super().__init__(config, extensions, log_queries, extra_nodes)

    async def run_inside_the_transaction(self, query: str, query_args: list, in_pool: bool):
        """
        Simple code wrapper, just for DRY

        Args:
            query: str
            query_args: list
            in_pool: bool

        """
        connection = self.transaction_connection.get()
        # We don`t test this block, becouse it`s already tested in original piccolo-orm
        if connection:
            return await connection.fetch(query, *query_args)  # pragma: no cover
        elif in_pool and self.pool:
            return await self._run_in_pool(query, query_args)  # pragma: no cover
        else:
            return await self._run_in_new_connection(query, query_args)

    async def run_querystring(
        self, querystring: QueryString, in_pool: bool = True
    ):

        query, query_args = querystring.compile_string(
            engine_type=self.engine_type
        )

        if self.log_queries:
            # No reason to test `print`
            print(querystring)  # pragma: no cover

        # If running inside a transaction:
        try:
            return await self.run_inside_the_transaction(
                query=query,
                query_args=query_args,
                in_pool=in_pool
            )
        except InvalidPasswordError:
            logger.warning(  # pragma: no cover
                'Failed to authenticate in DB server through Vault, obtaining new credentials')
            # Reloading db creds from vault, with adding to CONFIG instance
            # Was already tested directly
            await reload_db_creds()  # pragma: no cover
            # Setting new 'config' for PostgresEngine
            self.config = {'dsn': config.Database.get_connection_string()}
            # Retry of query with new creds
            return await self.run_inside_the_transaction(  # pragma: no cover
                query=query,
                query_args=query_args,
                in_pool=in_pool
            )
        except UndefinedTableError as ex:
            logger.error(  # pragma: no cover
                "Table not found, did you forget to `init` db or `run` migration?")
            logger.critical(f"Database error: {ex}")  # pragma: no cover


# First time building DB Engine
# Engine object is storing in CONFIG instance
# config.Database.set_connection_string('postgresql://test:test@127.0.0.1:5432/test')
# print(config.Database.build_connection_string)
config.Database.set_engine(
    PostgresEngine(
        config={
            'dsn': config.Database.get_connection_string(),
        },
        log_queries=bool(config.Main.log_sql)
    )
)
DB = config.Database.get_engine()


# A list of paths to piccolo apps
# e.g. ['blog.piccolo_app']
APP_REGISTRY = AppRegistry(
    apps=[
        "accounting.piccolo_app",
        "piccolo_admin.piccolo_app",
        "configuration.piccolo_app"
    ]
)
