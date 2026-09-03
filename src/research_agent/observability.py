from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

provider = TracerProvider()

processor = BatchSpanProcessor(
    ConsoleSpanExporter()
)

provider.add_span_processor(processor)

trace.set_tracer_provider(provider)

tracer = trace.get_tracer("research-agent")