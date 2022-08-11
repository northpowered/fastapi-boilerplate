from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.datastructures import MutableHeaders
import typing
import anyio
from uuid import uuid4
from logging import Filter, LogRecord
from typing import Optional
from contextvars import ContextVar

trace_id_context: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)
RequestResponseEndpoint = typing.Callable[[Request], typing.Awaitable[Response]]
DispatchFunction = typing.Callable[
    [Request, RequestResponseEndpoint], typing.Awaitable[Response]
]

class IDPropagationMiddleware():

    def __init__(self, app: ASGIApp, dispatch: typing.Optional[DispatchFunction] = None) -> None:
        self.app = app
        self.dispatch_func = self.dispatch if dispatch is None else dispatch
        self.tracing_header = "X-TRACE-ID"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        async def call_next(request: Request) -> Response:
            app_exc: typing.Optional[Exception] = None
            send_stream, recv_stream = anyio.create_memory_object_stream()

            async def coro() -> None:
                nonlocal app_exc

                async with send_stream:
                    try:
                        await self.app(scope, request.receive, send_stream.send)
                    except Exception as exc:
                        app_exc = exc

            task_group.start_soon(coro)

            try:
                message = await recv_stream.receive()
            except anyio.EndOfStream:
                if app_exc is not None:
                    raise app_exc
                raise RuntimeError("No response returned.")

            assert message["type"] == "http.response.start"

            async def body_stream() -> typing.AsyncGenerator[bytes, None]:
                async with recv_stream:
                    async for message in recv_stream:
                        assert message["type"] == "http.response.body"
                        yield message.get("body", b"")

                if app_exc is not None:
                    raise app_exc

            response = StreamingResponse(
                status_code=message["status"], content=body_stream()
            )
            response.raw_headers = message["headers"]
            return response

        async with anyio.create_task_group() as task_group:
            request = Request(scope, receive=receive)
            headers = MutableHeaders(scope=scope)
            #trace_id generates once at Request-Responce pair to propagate itself
            #to Request object of any endpoint and returns to Responce
            trace_id: str = uuid4().hex
            trace_id_context.set(trace_id)
            headers.append(self.tracing_header,trace_id)
            response = await self.dispatch_func(request, call_next)
            response.headers.append(self.tracing_header,trace_id)
            await response(scope, receive, send)
            task_group.cancel_scope.cancel()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
        ) -> Response:
        response = await call_next(request)
        return response


class CorrelationIdFilter(Filter):
    """Logging filter to attached correlation IDs to log records"""

    def __init__(self, name: str = '', uuid_length: Optional[int] = None):
        super().__init__(name=name)
        self.uuid_length = uuid_length

    def filter(self, record: LogRecord) -> bool:
        """
        Attach a correlation ID to the log record.
        Since the correlation ID is defined in the middleware layer, any
        log generated from a request after this point can easily be searched
        for, if the correlation ID is added to the message, or included as
        metadata.
        """
        cid = trace_id_context.get()
        if self.uuid_length is not None and cid:
            record.__setattr__('trace_id',cid[: self.uuid_length])
            #record.
            #record.correlation_id = cid[: self.uuid_length]
        else:
            record.__setattr__('trace_id',cid)
            #record.correlation_id = cid
        return True