import os
from dotenv import load_dotenv
from utils.currency_converter import CurrencyConverter
from langchain.tools import tool
from typing import List
load_dotenv()

class CurrencyConversionTool():
    def __init__(self):
        self.api_key=os.environ.get("EXCHANGE_RATE_API_KEY")
        self.currency_service_tool=CurrencyConverter(self.api_key)
        self.currency_converter_tool_list=self._setup_tools()
    
    def _setup_tools(self)->List:
        """Setup all tools for the currency converter tool"""
        @tool
        def convert_currency(amount:float,from_currency:str,to_currency:str):
            return self.currency_service_tool.convert(amount,from_currency,to_currency)
        
        return [convert_currency]