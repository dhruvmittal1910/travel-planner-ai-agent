from utils.model_loader import ModelLoader ##modelLoader is loading a llm model 
from prompts.prompts import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.calculate_cost_tool import CalculateCostTool
from tools.currency_conversion_tool import CurrencyConversionTool

class GraphBuilder():
    
    def __init__(self,model_provider:str="groq"):
        self.model_loader=ModelLoader(model_provider=model_provider)
        self.llm=self.model_loader.load_model()
        
        self.tools=[]
        
        self.weather_tool=WeatherInfoTool()
        self.place_search_tool=PlaceSearchTool()
        self.calculate_cost_tool=CalculateCostTool()
        self.currency_conversion_tool=CurrencyConversionTool()
        
        self.tools.extend([* self.weather_tool.weather_tool_list, 
                           * self.place_search_tool.place_search_tool_list,
                           * self.calculate_cost_tool.calculator_tool_list,
                           * self.currency_conversion_tool.currency_converter_tool_list])
        
        self.llm_with_tools=self.llm.bind_tools(tools=self.tools)
        self.graph=None
        self.system_prompt=SYSTEM_PROMPT
        
    
    def agent_function(self,state:MessagesState):
        # agent function handles some functionaloty.. we will be giving some instructuons or prompts to it too
        # agentic function acts as a brain and we pass an input
        # based on the input, it makes certain decisions.
        # either end the process with basic answer or it uses several tools
        # agentic function decision to the tool and then response from tool to agentic function and then again passing the reasonning to tools and back to agentic function, it runs in a loop
        # once we get final answer then only it stops
        # from agentic function to tool and tool to agentic function 
        
        # basically make decisions
        
        user_input=state['messages']
        llm_input=[self.system_prompt]+user_input
        response=self.llm_with_tools.invoke(llm_input)
        return {
            "messages":[response]
        }        
        
    
    def build_graph(self):
        graph_builder=StateGraph(MessagesState)
        
        # start adding nodes and edges
        # the agent node takses a decision what tool needs to be called
        graph_builder.add_node("agent",self.agent_function)
        # adding a node to give access to all available tools
        graph_builder.add_node("tools",ToolNode(tools=self.tools))
        graph_builder.add_edge(START,"agent")
        graph_builder.add_conditional_edges("agent",tools_condition)
        graph_builder.add_edge("tools","agent")
        graph_builder.add_edge("agent",END)
        
        self.graph=graph_builder.compile()
        
        return self.graph
        
        
    
    def __call__(self):
        return self.build_graph()
        