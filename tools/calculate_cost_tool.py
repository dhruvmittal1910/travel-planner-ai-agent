from typing import Lost
from langchain.tools import tool
from typing import List
from utils.calculator import ExpenseCalculator

class CalculateCostTool():
    def __init__(self):
        self.calculator=ExpenseCalculator()
        self.calculator_tool_list=self._setup_tools()
    
    def _setup_tools(self)->List:
        """Setup all tools for the calculator tool"""
        
        @tool
        def estimate_total_hotel_cost(price_per_night:float,total_days:int)->float:
            """Calculate total hotel cost"""
            return self.calculator.hotel_cost(price_per_night,total_days)
        
        @tool
        def calculate_total_expense(*costs:float)->float:
            """Calculate total expense of the trip"""
            return self.calculator.calculate_total_cost(*costs)
        
        @tool
        def calculate_daily_expense(total_cost:float,total_days:int)->float:
            return self.calculator.calculate_daily_budget(total_cost,total_days)
        
        return [estimate_total_hotel_cost,calculate_total_expense,calculate_daily_expense]