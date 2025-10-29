from dotenv import load_dotenv
import os
from typing import List
from langchain.tools import tool
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool

load_dotenv()

class PlaceSearchTool():
    
    def __init__(self):
        self.place_search_tool_list=self._setup_tools()
        self.google_api_key=os.environ.get("GPLACES_API_KEY")
        self.google_places_search=GooglePlaceSearchTool(self.google_api_key)
        self.tavily_search = TavilyPlaceSearchTool()
    
    def _setup_tools(self)->List:
        
        @tool
        def search_attractions(place:str)->str:
            """Search Attractions around that place"""
            try:
                result=self.google_places_search.google_search_attractions(place)
                if result:
                    return f"Following are the attractions around {place} as suggested by google: {result}"
                
            except Exception as e:
                result=self.tavily_search.tavily_search_attractions(place)
                return f"Following are the attractions around {place} : {result}"
    
        @tool
        def search_restraunts(place:str)->str:
            """Search Non Veg and Veg Restraunts around that area"""
            try:
                result=self.google_places_search.google_search_restraunts(place)
                if result:
                    return f"Following are the restraunts around {place} as suggested by google: {result}"
                
            except Exception as e:
                result=self.tavily_search.tavily_search_restraunts(place)
                return f"Following are the restraunts around {place} : {result}"
            
        @tool
        def search_activities(place:str)->str:
            """Search for Activities around that place to do"""
            try:
                result=self.google_places_search.google_search_activities(place)
                if result:
                    return f"Following are the top activities around {place} as suggested by google: {result}"
                
            except Exception as e:
                result=self.tavily_search.tavily_search_activities(place)
                return f"Following are the top activities around {place} : {result}"
            
        @tool
        def search_transportation(place:str)->str:
            """Search for transportation for traveling in and around that place"""
            try:
                result=self.google_places_search.google_search_transportation(place)
                if result:
                    return f"Following are the modes of transportation around {place} as suggested by google: {result}"
                
            except Exception as e:
                result=self.tavily_search.tavily_search_transportation(place)
                return f"Following are the modes of transporation around {place} : {result}"
            
        
        return [search_activities,search_attractions,search_restraunts,search_transportation]