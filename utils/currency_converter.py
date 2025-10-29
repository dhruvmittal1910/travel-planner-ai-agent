import requests


class CurrencyConverter():
    def __init__(self,api_key:str):
        self.base_url=f"https://v6.exchangerate-api.com/v6/{api_key}/latest"
    
    def convert(self,amount:int,from_curr:str,to_curr:str):
        """Convert the amount from one currency to another"""
        url=f"{self.base_url}/{from_curr}"
        response=requests.get(url)
        if response.status_code!=200:
            raise Exception("API call for conversion of currency failed")
        
        rates=response.json()['conversion_rates']
        if to_curr not in rates:
            raise ValueError(f"{to_curr} not found in exchange rates")
        
        return amount*rates[to_curr]