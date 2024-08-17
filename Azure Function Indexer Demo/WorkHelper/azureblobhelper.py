from langchain_community.document_loaders import AzureBlobStorageFileLoader
from langchain.docstore.document import Document

class AzureBlobHelper:
    def __init__(self,blob_service_client,connection_string) -> None:
        self.blob_service_client=blob_service_client
        self.connection_string=connection_string
        
        
    
    def CopyBlob(self,source_container_name, source_blob_name, dest_container_name, dest_blob_name):
        # Get the source and destination containers
        source_container = self.blob_service_client.get_container_client(source_container_name)
        dest_container = self.blob_service_client.get_container_client(dest_container_name)

        # Get the source blob
        source_blob = source_container.get_blob_client(source_blob_name)
        dest_blob = dest_container.get_blob_client(source_blob_name)
        
        # Start the copy operation        
        copy_blob_response = dest_blob.start_copy_from_url(source_blob.url)       
        
        if copy_blob_response['copy_status'] == 'success':
            print(f"Blob '{source_blob_name}' copied to '{dest_blob_name}' successfully.")
            dest_blob = dest_container.get_blob_client(source_blob_name)
            return dest_blob.url
        else:
            print(f"Error copying blob: {copy_blob_response.status_code}")
            return ''   
    
        
        
    def fnc_ProcessBolb(self,source_container_name, dest_container_name, source_blob_name)->list[Document]:
        _documents = []
        _source_blob_name = source_blob_name      
            
        _loader = AzureBlobStorageFileLoader(conn_str=self.connection_string, container=source_container_name, blob_name=_source_blob_name)
        _docs =_loader.load()
        _documents.extend(_docs) 
            
        _dest_blob_url = self.CopyBlob(source_container_name, source_blob_name, dest_container_name, source_blob_name)

        if _dest_blob_url != '':
            print(f"Blob '{source_blob_name}' copied to '{dest_container_name}' successfully.")            

            for _doc in _docs:
                #_doc.metadata['source'] = quote(_dest_blob_url+_sasToken)
                _doc.metadata['source'] = _dest_blob_url
                            
        else:
            print(f"Error copying blob: {_dest_blob_url}")

        return _docs
    
    def DelBlob(self,source_container_name,blobname): 
         # Get the source and destination containers
        _source_container_client = self.blob_service_client.get_container_client(source_container_name) 
        _source_container_client.delete_blob(blobname)
        print(f"Deleted Blob '{blobname}'... ")       
            