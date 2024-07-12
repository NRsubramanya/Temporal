from temporalio import activity
from eventception.sdk import EventceptionSDK
from pprint import pprint
import os

class BackendActivities:
    @activity.defn
    async def update_job_status(job: dict):
        eventception_api_client = EventceptionSDK(
            host = os.environ.get('EVENTCEPTION_URL'),
            username = os.environ.get('EVENTCEPTION_USERNAME'),
            password = os.environ.get('EVENTCEPTION_PASSWORD')
        )


        job_modified_response = await eventception_api_client.update_job(job['job_id'], job)
        pprint(job_modified_response)

        return job_modified_response
    
    @activity.defn
    async def create_logproducer_entity(data: dict):
        eventception_api_client = EventceptionSDK(
            host = os.environ.get('EVENTCEPTION_URL'),
            username = os.environ.get('EVENTCEPTION_USERNAME'),
            password = os.environ.get('EVENTCEPTION_PASSWORD')
        )

        payload = {
            "gateway": data["gateway_payload"]["uuid"], 
            "bootstrap_server": data["credential"]["bootstrap_server"], 
            "api_key": data["credential"]["kafka_api_key"], 
            "api_secret": data["credential"]["kafka_api_secret"], 
            "topic": data["logs_topic"], 
            "api_source_id": data["gateway_payload"]["unique_id"],
            "organization": data["gateway_payload"]["organization"]
        }

        cred_update_response = await eventception_api_client.create_push_logproducer(payload)

        return cred_update_response

    @activity.defn
    async def create_api_entity(data: dict):
        eventception_api_client = EventceptionSDK(
            host = os.environ.get('EVENTCEPTION_URL'),
            username = os.environ.get('EVENTCEPTION_USERNAME'),
            password = os.environ.get('EVENTCEPTION_PASSWORD')
        )

        api = {
            "name": data["api_name"],
            "api_id": data["gateway_id"]+"-"+data["api_name"],
            "description": "Route for service ID - "+data["service_id"],
            "apitype": "rest",
            "hostname": data["hostname"],
            "basepath": data["path"],
            "gateway": data["gateway_uuid"],
            "organization": data["organization_uuid"]
        }

        api_create_response = await eventception_api_client.create_api(api, data["gateway_id"])

        return api_create_response

    @activity.defn
    async def get_gateway_id(data: dict):
        eventception_api_client = EventceptionSDK(
            host = os.environ.get('EVENTCEPTION_URL'),
            username = os.environ.get('EVENTCEPTION_USERNAME'),
            password = os.environ.get('EVENTCEPTION_PASSWORD')
        )

        return await eventception_api_client.get_gateway_id(data["org_uuid"], data["gateway_uuid"])

    @activity.defn
    async def update_stream_bootstrap_servers(data: dict):
        eventception_api_client = EventceptionSDK(
            host = os.environ.get('EVENTCEPTION_URL'),
            username = os.environ.get('EVENTCEPTION_USERNAME'),
            password = os.environ.get('EVENTCEPTION_PASSWORD')
        )

        data["bootstrapservers"] = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")

        org_id = data["org_unique_id"]
        gateway_id = data["gateway_unique_id"]

        del data["org_uuid"]
        del data["gateway_unique_id"]
        del data["org_unique_id"]

        return await eventception_api_client.update_stream(org_id, gateway_id, data)

    @activity.defn
    async def create_kafka_consumer_api_key_entity(data: dict):
        eventception_api_client = EventceptionSDK(
            host = os.environ.get('EVENTCEPTION_URL'),
            username = os.environ.get('EVENTCEPTION_USERNAME'),
            password = os.environ.get('EVENTCEPTION_PASSWORD')
        )

        gateway_pushlogproducers = await eventception_api_client.get_push_logproducer(data["org_unique_id"], data["gateway_unique_id"])

        kafka_consumer_api_key = {
            "name": data["name"]+"-api-key",
            "user_email": data["user_email"],
            "stream": data["uuid"],
            "sasl_username": gateway_pushlogproducers["results"][0]["api_key"],
            "sasl_password": gateway_pushlogproducers["results"][0]["api_secret"]
        }


        return await eventception_api_client.create_kafka_consumer_api_key(data["org_unique_id"], kafka_consumer_api_key)

    @activity.defn
    async def update_eventprocessor_entity(data: dict):
        eventception_api_client = EventceptionSDK(
            host = os.environ.get('EVENTCEPTION_URL'),
            username = os.environ.get('EVENTCEPTION_USERNAME'),
            password = os.environ.get('EVENTCEPTION_PASSWORD')
        )

        org_id = data["org_unique_id"]
        gateway_id = data["gateway_unique_id"]

        del data["org_uuid"]
        del data["gateway_uuid"]
        del data["gateway_unique_id"]
        del data["org_unique_id"]
        del data["api_id"]

        return await eventception_api_client.update_eventprocessor(org_id, gateway_id, data)
    
    @activity.defn
    async def create_stream_entity(data: dict):
        eventception_api_client = EventceptionSDK(
            host = os.environ.get('EVENTCEPTION_URL'),
            username = os.environ.get('EVENTCEPTION_USERNAME'),
            password = os.environ.get('EVENTCEPTION_PASSWORD')
        )

        org_id = data["org_id"]
        gateway_id = data["gateway_id"]

        del data["org_id"]
        del data["gateway_id"]

        return await eventception_api_client.create_stream(org_id, gateway_id, data)