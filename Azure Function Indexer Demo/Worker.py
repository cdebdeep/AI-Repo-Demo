from azure.storage.blob import BlobServiceClient
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

from WorkHelper.azureaihelper import AzureAIHelper
from WorkHelper.azureblobhelper import AzureBlobHelper


        

def fnc_ProcessBlobSequ(azureAIHelper:AzureAIHelper,azureBlobHelper:AzureBlobHelper,blob_service_client,source_container_name, dest_container_name,chunkSize:int,chunkOverLap:int):
    
    _blob_service_client = blob_service_client 
     # Get the source and destination containers
    _source_container_client = _blob_service_client.get_container_client(source_container_name)    
    # List all blobs in the container
    _blobs = _source_container_client.list_blobs()
    
    try:       
        
        for blob in _blobs:
                        
            #_blobname=blob.name.replace('\u200b', '')
            _blobname=blob.name
            
            print(f"Processing Blob '{_blobname}'... ")
            
            
            _docs= azureBlobHelper.fnc_ProcessBolb(source_container_name, dest_container_name,_blobname)

            if _docs:
                azureAIHelper.fnc_AddDocToVectorDB(_docs,chunkSize,chunkOverLap)
                azureBlobHelper.DelBlob(source_container_name,_blobname)          
                
                print(f"Processing Complete for Blob '{_blobname}'... ")              
        
        
        return 'Ok'
    except Exception as e:
        message = str(e)
        logging.error(f"Exception in processing the Blob: {message}")     
        
        raise e




def Do_Work(): 
    # Load environment variables from .env file
    load_dotenv()
# Access the environment variable
    _envname = os.getenv('ENV_NAME')
    print(f'MySettingName: {_envname}')
    
    try:      
               
        _connection_string = os.getenv('STORAGE-CONSTR')         
       
        
        #Initialize the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(_connection_string)
        

        _pdf_source_container_name = os.getenv('STORAGE_PDF_SOURCE_CONTAINER_NAME')
        _pdf_dest_container_name = os.getenv('STORAGE_PDF_DEST_CONTAINER_NAME')

    

        _azureOpenAIKey=os.getenv('OPENAI-APIKEY')
        _azureOpenAIEndPoint=os.getenv('OPENAI-ENDPOINT')        
        
        
        _azureDeplyModel=os.getenv('OPENAI_AZURE_DEPLOYMENT')
        _openApiVersion=os.getenv('OPENAI_OPENAI_API_VERSION')

        _vector_store_address: str = os.getenv('OPENAI-VECTORSTOREADDRESS')
        _vector_store_password: str = os.getenv('OPENAI-VECTORSTOREPASSWORD')       
        

       
        _pdf_indexName=os.getenv('PDF_Index_Name')
       
        _doc_chunkSize=os.getenv('OPENAI_DOC_CHUNKSIZE')
        _doc_chunkOverlap=os.getenv('OPENAI_DOC_CHUNKOVERLAP')

        _AzureAIHelper = AzureAIHelper(_azureOpenAIKey, _azureOpenAIEndPoint, _azureDeplyModel, _openApiVersion, _vector_store_address, _vector_store_password)
        _AzureBlobHelper= AzureBlobHelper(blob_service_client,_connection_string)
        
        
        _stTime= datetime.now().strftime("%H:%M:%S")
        print(f"Processing Started at: '{_stTime}'... ")        
       
        
        _embedding= _AzureAIHelper.fnc_getEmbedding()   

        _vectorDBPdf= _AzureAIHelper.fnc_getVectorDB(_pdf_indexName,_embedding)        
        
        #Process PDF        
        _retVal=fnc_ProcessBlobSequ(_AzureAIHelper,_AzureBlobHelper,blob_service_client, _pdf_source_container_name, _pdf_dest_container_name,_doc_chunkSize,_doc_chunkOverlap)
        if _retVal == 'Ok':    
            print(f"Processing Complete for PDF Blob. Index generated as: '{_vectorDBPdf}'... ")            
            
        _endTime= datetime.now().strftime("%H:%M:%S")
        print(f"Processing Ended at: '{_endTime}'... ")     
    
        return 'Ok'
    
    except Exception as e:
        message = str(e)
        print(f"Caught an exception: {message}")       
        raise e

  



  

    

       
    
    
    
   
    
          
          