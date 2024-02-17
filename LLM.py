from abc import ABC, abstractmethod
import os

class LLM(ABC):
    @abstractmethod
    def get(self, typ) -> object:
        """
        Get the LLM object.
        
        typ: 'light' or 'heavy'
        return an object
        """
        pass

class Anthropic(LLM):
    def get(self, typ='light', max_token=500):
        from utils import bedrock
        from langchain.llms.bedrock import Bedrock
        boto3_bedrock = bedrock.get_bedrock_client(
            assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
            region=os.environ.get("AWS_DEFAULT_REGION", None)
        )
        
        if typ not in ['light', 'heavy']:
            raise ValueError(f"Invalid type. Expected one of: {'light', 'heavy'}")
            
        if typ == 'light':
            the_model='anthropic.claude-instant-v1'
            print(f'\n===== INITIATING LLM: {the_model} =====')
            return Bedrock(model_id=the_model, client=boto3_bedrock, model_kwargs={'max_tokens_to_sample':max_token, 'temperature': 0.3})  
        else:
            the_model='anthropic.claude-v2'
            print(f'\n===== INITIATING LLM: {the_model} =====')
            return Bedrock(model_id=the_model, client=boto3_bedrock, model_kwargs={'max_tokens_to_sample':max_token, 'temperature': 0.3})   

class Meta(LLM):
    def get(self, typ='light'):
        from utils import bedrock
        from langchain.llms.bedrock import Bedrock
        boto3_bedrock = bedrock.get_bedrock_client(
            assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
            region=os.environ.get("AWS_DEFAULT_REGION", None)
        )
        
        the_model='meta.llama2-13b-chat-v1'
        print(f'\n===== INITIATING LLM: {the_model} =====')
        return Bedrock(model_id=the_model, client=boto3_bedrock, model_kwargs={'max_tokens_to_sample':200}) 
        
    
class Titan(LLM):
    def get(self, typ='light'):
        from utils import bedrock
        from langchain.llms.bedrock import Bedrock
        boto3_bedrock = bedrock.get_bedrock_client(
            assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
            region=os.environ.get("AWS_DEFAULT_REGION", None)
        )
        
        if typ not in ['light', 'heavy']:
            raise ValueError(f"Invalid type. Expected one of: {'light', 'heavy'}")
            
        if typ == 'light':
            the_model='amazon.titan-text-lite-v1'
            print(f'\n===== INITIATING LLM: {the_model} =====')
            return Bedrock(model_id=the_model, client=boto3_bedrock, model_kwargs={'max_tokens_to_sample':200})  
        else:
            the_model='amazon.titan-text-express-v1'
            print(f'\n===== INITIATING LLM: {the_model} =====')
            return Bedrock(model_id=the_model, client=boto3_bedrock, model_kwargs={'max_tokens_to_sample':200}) 