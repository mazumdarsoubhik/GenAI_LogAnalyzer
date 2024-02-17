from abc import ABC, abstractmethod
import os

class VectorDB(ABC):
    @abstractmethod
    def getVectorDB(self, path: str) -> object:
        pass

    
class FAISS_VDB(VectorDB):
    def __init__(self, directory):
        """
        Initiate the object with the server or application framework e.g. dotnet, ibmbpm, linux etc
        """
        self.directory=f'data/{directory}'
        
    def getVectorDB(self):
        import numpy as np
        from langchain.vectorstores import FAISS
        from langchain.indexes import VectorstoreIndexCreator
        from langchain.indexes.vectorstore import VectorStoreIndexWrapper
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
        from langchain.embeddings import BedrockEmbeddings
        from utils import bedrock
        
        boto3_bedrock = bedrock.get_bedrock_client(
            assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
            region=os.environ.get("AWS_DEFAULT_REGION", None)
        )
        bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=boto3_bedrock)
        
        print(f'\n===== INITIATING FAISS VECTOR DB for {self.directory} framework=====')
        
        # Load all the Manuals
        print(f'Manuals dir: {self.directory}')
        loader = PyPDFDirectoryLoader(self.directory)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap  = 100,
        )
        
        docs = text_splitter.split_documents(documents)

        print(f'Loaded --{self.directory}-- manuals with total {len(docs)} pages')
        
        # Embedding Heartbeat check
        try:
            sample_embedding = np.array(bedrock_embeddings.embed_query(docs[0].page_content))
            print(f'Sample embedding of a document chunk: {sample_embedding}\nSize of the embedding: {sample_embedding.shape}')
        except ValueError as error:
            if  "AccessDeniedException" in str(error):
                print(f"\x1b[41m{error}\
                \nTo troubeshoot this issue please refer to the following resources.\
                 \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                 \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")      
                class StopExecution(ValueError):
                    def _render_traceback_(self):
                        pass
                raise StopExecution        
            else:
                raise error
        
        # Insert embeddings
        print("Inserting vectors into vector DB...")
        vectorstore_faiss = FAISS.from_documents(
            docs,
            bedrock_embeddings,
        )
        wrapper_store_faiss = VectorStoreIndexWrapper(vectorstore=vectorstore_faiss)
        print('===== END OF VECTOR LOADING =====\n')
        
        return vectorstore_faiss
    
    
class Chroma_VDB(VectorDB):
    def getVectorDB(self, path: str):
        pass