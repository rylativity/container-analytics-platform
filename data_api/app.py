from typing import List, Union
from fastapi import FastAPI
import json

from introspect_trino import ModelEndpointFactory

app = FastAPI(debug=True)

for route, model in ModelEndpointFactory(trino_host='trino').generate_api_routes_and_models().items():
    
    @app.get(route, response_model=Union[List[model], model])
    def func():
        if "taxi" in route:
            with open("./sample_taxi_response.json") as f:
                resp = json.load(f)
            return resp
        return f"Created route at {route} for model {model.__name__}"
    globals()[f"api_route_{model.__name__}"] = func()
