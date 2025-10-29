import os
from typing import List
from dotenv import load_dotenv
# from utils.weather_info import WeatherForecastTool
from langchain.tools import tool
from pydantic import BaseModel
from utils.weather_info import WeatherForecastTool

load_dotenv()


class WeatherInfoTool():
    
    def __init__(self):
        self.api_key=os.environ.get("OPENWEATHERMAP_API_KEY")
        self.weather_service=WeatherForecastTool(self.api_key)
        # below will give me all the tools available for the functionality
        self.weather_tool_list=self._setup_tools()
        
    def _setup_tools(self)->list:
        
    
        @tool
        def get_current_weather(city:str)->str:
            """
            Get the real time weather or the weather on specific date of the given city
            
            
            """
            weather_data=self.weather_service.get_current_weather(city)
            if weather_data:
                temp=weather_data.get("main",{}).get("temp","N/A")
                desc=weather_data.get("weather",[{}])[0].get("description","N/A")
                return f"Current Weather in {city} : {temp}°C, {desc}"
            return f"Could not fetch {city}'s weather data"

        @tool 
        def get_weather_forecast(city:str)->str:
            
            forecast_data=self.weather_service.get_forecast_weather(city)
            if forecast_data and "list" in forecast_data:
                forecast_summary=[]
                for i in range(len(forecast_data['list'])):
                    item=forecast_data['list'][i]
                    data=item['dt_txt'].split(' ')[0]
                    temp=item['main']['temp']
                    desc=item['weather'][0]['description']
                    forecast_summary.append(
                        f"{data}:{temp} degress celcius, {desc}"
                    )
                return f"Weather forecast for {city}:\n"+"\n".join(forecast_summary)
            return f"Could not fetch forecast data for {city}"
                

        return [get_current_weather,get_weather_forecast]
    