from functools import reduce
import json

import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    input_context = context.get_input()

    tasks = []
    for x in input_context.get('urls'):
        tasks.append(context.call_activity('DetectFace', x))

    result = yield context.task_all(tasks)
    
    flatten_list = reduce(lambda a, b: a+b, filter(lambda x: x is not None, result))

    return {
        "min_val": min(flatten_list),
        "max_val": max(flatten_list)
    }

main = df.Orchestrator.create(orchestrator_function)
