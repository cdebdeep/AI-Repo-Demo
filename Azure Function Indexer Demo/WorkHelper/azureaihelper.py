
#from langchain.document_loaders import AzureBlobStorageFileLoader
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

from langchain.docstore.document import Document




class AzureAIHelper:
    def __init__(self,azureOpenAIKey,azureOpenAIEndPoint,azureDeplyModel,openApiVersion,vector_store_address,vector_store_password) -> None:        
        
        self.azureOpenAIKey = azureOpenAIKey
        self.azureOpenAIEndPoint = azureOpenAIEndPoint
        self.azureDeplyModel = azureDeplyModel
        self.openApiVersion = openApiVersion
        self.vector_store_address = vector_store_address
        self.vector_store_password = vector_store_password
        
        
        
    def fnc_getEmbedding(self)->AzureOpenAIEmbeddings:
        _embeddings = AzureOpenAIEmbeddings(
        azure_deployment=self.azureDeplyModel,
        openai_api_version=self.openApiVersion,
        api_key=self.azureOpenAIKey,
        azure_endpoint=self.azureOpenAIEndPoint
            )
        print('fnc_getEmbedding')        
        return _embeddings 
    
    
    def fnc_getVectorDB(self,indexName,embedding:AzureOpenAIEmbeddings)->AzureSearch:
        vector_store: AzureSearch = AzureSearch(
        azure_search_endpoint=self.vector_store_address,
        azure_search_key=self.vector_store_password,
        index_name=indexName,
        embedding_function=embedding.embed_query,
        ) 
        self.vectorDB= vector_store    
        return vector_store  
    
    
    def fnc_AddDocToVectorDB(self,docList:list[Document],chunkSize:int,chunkOverLap:int)->AzureSearch:
        #_characterTextSplitter = CharacterTextSplitter(chunk_size=chunkSize, chunk_overlap=chunkOverLap)
        _characterTextSplitter = CharacterTextSplitter(separator="\n\n")
        _docs = _characterTextSplitter.split_documents(docList)

        self.vectorDB.add_documents(documents=_docs)         
        return self.vectorDB  
    
    
    