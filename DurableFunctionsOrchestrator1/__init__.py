# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

from ctypes import resize
import logging
import json
from unittest import result

import azure.functions as func
import azure.durable_functions as df
from ExtractDFS.dataforseo import dataforseo
import azure.functions as func
import logging
from shared_code.storage_functions import AzureStorage
import pandas as pd


def orchestrator_function(context: df.DurableOrchestrationContext):
    
    urls_list=[]
    new_site_list=["https://cricbuzz.com/","https://aryzap.com/","https://www.hotstar.com/","https://twitter.com","https://youtube.com","https://www.pcb.com","https://www.triplek.tech","https://www.beingguru.com"]
    # new_site_list = json.loads(site_list)
    tasks = []
    for url in new_site_list:
        urls_list.append(url)
        input_config = {
        "container_name":"dev-1",
        "timestamp":"2022-09-25",
        "new_site_list":urls_list
    }
        
        tasks.append(context.call_activity("ExtractDFS", input_config))
    results = yield context.task_all(tasks)
    # json.dump(results)
    print(f"Final Results:  {results}")
    input_config = {
        "container_name":"dev-1",
        "timestamp":"2022-09-25"
    }
    azs = AzureStorage(input_config["container_name"])
    function_name = "dataforseo"
    path = "{0}/{1}/{1}_{2}_{0}.csv".format(input_config["timestamp"], function_name, input_config["container_name"])
    results = pd.DataFrame(results)

    azs.upload_blob_df(results, path)
    return("Working fine")

main = df.Orchestrator.create(orchestrator_function)