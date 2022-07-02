import os
import logging
from loguru import logger
import os
from configuration import config
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        
        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
        

def setup_logging():
    """
    concurrent.futures
    concurrent
    asyncio
    fastapi
    urllib3.util.retry
    urllib3.util
    urllib3
    urllib3.connection
    urllib3.response
    urllib3.connectionpool
    urllib3.poolmanager
    charset_normalizer
    requests
    sqlalchemy
    sqlalchemy.orm.path_registry
    sqlalchemy.orm
    sqlalchemy.orm.relationships.RelationshipProperty
    sqlalchemy.orm.relationships
    sqlalchemy.orm.properties.ColumnProperty
    sqlalchemy.orm.properties
    sqlalchemy.orm.mapper.Mapper
    sqlalchemy.orm.mapper
    sqlalchemy.orm.query.Query
    sqlalchemy.orm.query
    sqlalchemy.orm.strategies.ColumnLoader
    sqlalchemy.orm.strategies
    sqlalchemy.orm.strategies.ExpressionColumnLoader
    sqlalchemy.orm.strategies.DeferredColumnLoader
    sqlalchemy.orm.strategies.DoNothingLoader
    sqlalchemy.orm.strategies.NoLoader
    sqlalchemy.orm.strategies.LazyLoader
    sqlalchemy.orm.strategies.SubqueryLoader
    sqlalchemy.orm.strategies.JoinedLoader
    sqlalchemy.orm.strategies.SelectInLoader
    sqlalchemy.orm.dynamic.DynaLoader
    sqlalchemy.orm.dynamic
    parse
    sqlalchemy.dialects.postgresql
    sqlalchemy.dialects
    asyncpg.pool
    asyncpg
    sqlalchemy.pool.impl.AsyncAdaptedQueuePool
    sqlalchemy.pool.impl
    sqlalchemy.pool
    sqlalchemy.engine.Engine
    sqlalchemy.engine
    uvicorn.error
    uvicorn
    watchgod.watcher
    watchgod
    watchgod.main
    exporter
    opentelemetry.context
    opentelemetry
    opentelemetry.attributes
    opentelemetry.trace.status
    opentelemetry.trace
    opentelemetry.trace.span
    opentelemetry.util._providers
    opentelemetry.util
    opentelemetry.exporter.jaeger.thrift.send
    opentelemetry.exporter.jaeger.thrift
    opentelemetry.exporter.jaeger
    opentelemetry.exporter
    opentelemetry.sdk.resources
    opentelemetry.sdk
    opentelemetry.sdk.trace.sampling
    opentelemetry.sdk.trace
    opentelemetry.sdk.trace.export
    opentelemetry.propagators.composite
    opentelemetry.propagators
    opentelemetry.propagate
    opentelemetry.util.re
    opentelemetry.baggage
    opentelemetry.baggage.propagation
    opentelemetry.instrumentation.dependencies
    opentelemetry.instrumentation
    opentelemetry.instrumentation.instrumentor
    opentelemetry.instrumentation.fastapi
    concurrent.futures
    concurrent
    asyncio
    fastapi
    urllib3.util.retry
    urllib3.util
    urllib3
    urllib3.connection
    urllib3.response
    urllib3.connectionpool
    urllib3.poolmanager
    charset_normalizer
    requests
    sqlalchemy
    sqlalchemy.orm.path_registry
    sqlalchemy.orm
    sqlalchemy.orm.relationships.RelationshipProperty
    sqlalchemy.orm.relationships
    sqlalchemy.orm.properties.ColumnProperty
    sqlalchemy.orm.properties
    sqlalchemy.orm.mapper.Mapper
    sqlalchemy.orm.mapper
    sqlalchemy.orm.query.Query
    sqlalchemy.orm.query
    sqlalchemy.orm.strategies.ColumnLoader
    sqlalchemy.orm.strategies
    sqlalchemy.orm.strategies.ExpressionColumnLoader
    sqlalchemy.orm.strategies.DeferredColumnLoader
    sqlalchemy.orm.strategies.DoNothingLoader
    sqlalchemy.orm.strategies.NoLoader
    sqlalchemy.orm.strategies.LazyLoader
    sqlalchemy.orm.strategies.SubqueryLoader
    sqlalchemy.orm.strategies.JoinedLoader
    sqlalchemy.orm.strategies.SelectInLoader
    sqlalchemy.orm.dynamic.DynaLoader
    sqlalchemy.orm.dynamic
    parse
    sqlalchemy.dialects.postgresql
    sqlalchemy.dialects
    asyncpg.pool
    asyncpg
    sqlalchemy.pool.impl.AsyncAdaptedQueuePool
    sqlalchemy.pool.impl
    sqlalchemy.pool
    sqlalchemy.engine.Engine
    sqlalchemy.engine
    uvicorn.error
    uvicorn
    watchgod.watcher
    watchgod
    watchgod.main
    exporter
    opentelemetry.context
    opentelemetry
    opentelemetry.attributes
    opentelemetry.trace.status
    opentelemetry.trace
    opentelemetry.trace.span
    opentelemetry.util._providers
    opentelemetry.util
    opentelemetry.exporter.jaeger.thrift.send
    opentelemetry.exporter.jaeger.thrift
    opentelemetry.exporter.jaeger
    opentelemetry.exporter
    opentelemetry.sdk.resources
    opentelemetry.sdk
    opentelemetry.sdk.trace.sampling
    opentelemetry.sdk.trace
    opentelemetry.sdk.trace.export
    opentelemetry.propagators.composite
    opentelemetry.propagators
    opentelemetry.propagate
    opentelemetry.util.re
    opentelemetry.baggage
    opentelemetry.baggage.propagation
    opentelemetry.instrumentation.dependencies
    opentelemetry.instrumentation
    opentelemetry.instrumentation.instrumentor
    opentelemetry.instrumentation.fastapi
    uvicorn.access
    """
    logging.root.handlers = [InterceptHandler()]

    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
        sql_logging = str(name).startswith('sqlalchemy') | config.main.log_sql
        if not sql_logging:
            logging.getLogger(name).setLevel(config.main.log_level)
        

    logger.configure(
        handlers=[
            {
                "sink": config.main.log_sink, 
                "serialize": config.main.log_in_json, 
                "level":config.main.log_level
            }
        ]
    )
    logger.add(lambda _: os._exit(0), level="CRITICAL")