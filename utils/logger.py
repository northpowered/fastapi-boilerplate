import os
import logging
from loguru import logger
from configuration import config
from .id_propagation import TraceIdFilter

TRACE_ID_LENGTH: int = 12 #Replace to config file
class InterceptHandler(logging.Handler):
    def emit(self, record):
        extra_data: dict = dict()
        try:
            #Trying to catch `trace_id` and exclude None, if cought
            assert record.trace_id
            extra_data['trace_id'] = record.trace_id
        except (AttributeError, AssertionError):
            pass
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
        #Inject `extra` payload to `message` dict
        log = logger.bind(**extra_data)
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
        

def setup_logging():
    logging.root.handlers = [InterceptHandler()]

    for name in logging.root.manager.loggerDict.keys():
        _logger = logging.getLogger(name)
        _logger.handlers = []
        _logger.propagate = True
        _logger.setLevel(config.main.log_level)
        if name.startswith('uvicorn'):
            _logger.addFilter(TraceIdFilter(uuid_length=TRACE_ID_LENGTH))
        
    def formatter(record):
        base_fmt = "<green>{time:YYYY-MM-DDTHH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{module: <16}</cyan>"
        extra: dict = record.get('extra',dict())
        try:
            trace_id = extra['trace_id']
            base_fmt = base_fmt + f" | [{trace_id}]"
        except KeyError:
            pass
        return base_fmt + " | <level>{message}</level>\n"
    logger.configure(
        handlers=[
            {
                "sink": config.main.log_sink, 
                "serialize": config.main.log_in_json, 
                "level":config.main.log_level,
                "format":formatter,
                "colorize":True
            }
        ]
    )
    logger.add(lambda _: os._exit(0), level="CRITICAL")