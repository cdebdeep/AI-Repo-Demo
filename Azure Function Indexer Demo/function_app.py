import azure.functions as func
from azure.functions import AuthLevel
import logging
from dotenv import load_dotenv
import os

import Worker as worker

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="Indexer")
def Indexer(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')
    
    # Load environment variables from .env file
    load_dotenv()
    _envname = os.getenv('ENV_NAME')
    print(f'MySettingName: {_envname}')
    logging.info('Application Env is: ' + _envname)          
           
         
    
    try:

    
        __retVal = worker.Do_Work()
        
        if __retVal=='Ok':
            return func.HttpResponse(
                    "This Indexer  function executed successfully.",
                    status_code=200
                )
        else:
            return func.HttpResponse(
                    "This Indexer function failed.",
                    status_code=500
                )
    except Exception as e:
        print(f"Exception!! . An error: {e}")
        
        return func.HttpResponse(
                "Error...",
                status_code=500
        )         

    
    