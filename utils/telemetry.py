from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from configuration import config
from loguru import logger

def server_request_hook(span, scope: dict):
    if span and span.is_recording():
        pass


def client_request_hook(span, scope: dict):
    if span and span.is_recording():
        pass


def client_response_hook(span, message: dict):
    if span and span.is_recording():
        pass


def enable_tracing(app):
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: app.title})
        )
    )
    
    jaeger_exporter = JaegerExporter(
        # configure agent
        agent_host_name=config.Telemetry.agent_host,
        agent_port=config.Telemetry.agent_port,        # optional: configure also collector
        # collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
        # username=xxxx, # optional
        # password=xxxx, # optional
        # max_tag_value_length=None # optionalormat=jaeger.thrift',
        # username=xxxx, # optional
        # password=xxxx, # optional
        # max_tag_value_length=None # optional
    )

    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    FastAPIInstrumentor.instrument_app(app)
    FastAPIInstrumentor().instrument(
        server_request_hook=server_request_hook,
        client_request_hook=client_request_hook, 
        client_response_hook=client_response_hook
    )
    logger.info(f'Telemetry exporter to {config.Telemetry.agent_host}:{config.Telemetry.agent_port} for {config.Telemetry.agent_type} enabled')
tracer = trace.get_tracer(__name__)