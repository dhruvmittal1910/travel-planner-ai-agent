# loading the models here
from pydantic import BaseModel, Field
from typing import Dict,Any, List
import os, sys
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# class ConfigLoader():
#     def __init__(self):
#         print("Calling to load the model config")
#         self.config=load_config()
    
#     def __getitem__(self,key):
#         return self.config[key]
    
    

class ModelLoader(BaseModel):
    model_provider:str="groq"
    # load the config for llm models
    config: Dict[str, Any]=Field(default_factory=load_config, exclude=True)
    
    class Config:
        arbitrary_types_allowed=True
    
    
    def load_model(self):
        """ load the llm model here"""
        
        print("-----Loading LLM model------")
        print(f"model loading from : {self.model_provider} ")
        
        llm_config=self.config['llm'][self.model_provider]
        model_name=llm_config['model']
        api_key=llm_config.get("apikey") or os.getenv(f"{self.model_provider.upper()}_API_KEY")
        
        if not api_key:
            raise ValueError("Api key not mentioned in config.yaml file")
        
        if self.model_provider=='groq':
            print("----Loading model from GROQ-----")
            llm=ChatGroq(
                model=model_name,
                api_key=api_key
            )
        else:
            print("----Loading Open AI model----")
            llm=ChatOpenAI(
                model=model_name,
                api_key=api_key
            )
        
        
        return llm
        