
# creating endpoints
from fastapi import FastAPI
from grpc import StatusCode
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
import os
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query:str

@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    # take user query
    # call the graph builder too
    try:
        
        print("--------Query-------\n",query)
        graph=GraphBuilder(model_provider='groq')
        reactive_app=graph()

        # save the graph created
        save_graph=reactive_app.get_graph().draw_mermaid_png()
        with open("agentic_graph_image.png","wb") as file:
            file.write(save_graph)

        print(f"-----Graph saved to agentic_graph_image.png file in {os.getcwd()}------")

        # assuming the user query is of format {"question":"user input"}
        user_message={"messages":[query.question]}
        # insert this user message to llm
        output=reactive_app.invoke(user_message)

        # if the output is a dict then give output as below
        if isinstance(output,dict) and "messages" in output:
            final_output=output["messages"][-1].content
        else:
            final_output=str(output)

        return {
            "answer":final_output
        }
    except Exception as e:
        print("Exception occurred in post request to query endpoint, check")
        return e
    
