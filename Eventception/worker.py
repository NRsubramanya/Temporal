import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

import os
from dotenv import load_dotenv

from activities.backend import BackendActivities
from activities.kafka import KafkaResources
from activities.kubernetes import K8sResources
from activities.kong import KongResources
from activities.stream import StreamActivities
from activities.auth0_org import create_auth0_org
from workflows.create_organization import CreateOrganization
from workflows.create_gateway import CreateGateway
from workflows.sync_gateway import SyncGateway
from workflows.create_stream import CreateStream
from workflows.create_eventprocessor import CreateEventprocessor
from temporalio.worker import Interceptor
from interceptor import EventInterceptor

async def main():
    load_dotenv()
    client = await Client.connect(os.environ.get('TEMPORAL_ADDRESS'))

    # Run the worker

    worker = Worker(
        client,
        task_queue="eventception-tasks",
        workflows=[
            CreateOrganization,
            CreateGateway,
            SyncGateway,
            CreateStream,
            CreateEventprocessor
        ],
        activities=[
            BackendActivities.update_job_status,
            BackendActivities.create_logproducer_entity,
            BackendActivities.create_api_entity,
            BackendActivities.get_gateway_id,
            BackendActivities.update_stream_bootstrap_servers,
            BackendActivities.create_kafka_consumer_api_key_entity,
            BackendActivities.update_eventprocessor_entity,
            BackendActivities.create_stream_entity,
            create_auth0_org.create_org,
            KafkaResources.create_logproducer_topic,
            KafkaResources.create_logproducer_credential,
            KafkaResources.create_stream_topic,
            K8sResources.create_gateway_namespace,
            K8sResources.create_connect_cluster,
            K8sResources.create_flink_resources,
            K8sResources.deploy_flink_job,
            KongResources.get_routes,
            StreamActivities.get_spec_from_url
        ],
        interceptors=[EventInterceptor()],
    )
    print("Starting the worker....")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
