import asyncio
import os
import sentry_sdk
from temporalio import activity, workflow

from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.contrib.opentelemetry import TracingInterceptor  # Assuming you have this defined correctly
from translate import TranslateActivities
from greeting import GreetSomeone
from opentelemetry import trace
import opentelemetry.context
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from temporalio.worker import Interceptor
from interceptor import _WorkflowInterceptor
from temporalio.worker import (
    Interceptor,
    WorkflowInboundInterceptor,
    WorkflowInterceptorClassInput,
)
from interceptor import SentryInterceptor


async def main():

    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
    )
    # Connect to Temporal server
    client = await Client.connect("localhost:7233", namespace="default")

    # Create an instance of TranslateActivities without session
    activities = TranslateActivities()

    # Create a worker with tracing interceptor
  
    worker = Worker(
        client,
        task_queue="greeting-tasks",
        workflows=[GreetSomeone],
        activities=[activities.greet_in_spanish, activities.farewell_in_spanish],
        interceptors=[SentryInterceptor()],
    )

    print("Starting the worker....")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
