import json
import logging

import azure.functions as func
import azure.durable_functions as df


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    fn_name = req.route_params["functionName"]

    if fn_name == "Orchestrator":
        urls = json.loads(req.get_body())
        instance_id = await client.start_new(fn_name, None, {"urls": urls})
    else:
        instance_id = await client.start_new(fn_name, None, None)
        
    logging.info(f"Started orchestration with ID = '{instance_id}'.")
    return client.create_check_status_response(req, instance_id)
