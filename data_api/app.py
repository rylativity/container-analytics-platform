from typing import List, Optional, Union
from fastapi import FastAPI
import json

from introspect_trino import ModelEndpointFactory, TrinoDriver

TRINO_HOST = 'trino'

app = FastAPI(debug=True)
driver = TrinoDriver(trino_host=TRINO_HOST)

for route, model in ModelEndpointFactory(trino_host=TRINO_HOST).generate_api_routes_and_models().items():

    schema_name, table_name = route.split("/")[-2:]
    
    @app.get(route, response_model=Union[List[model], model])
    def func(limit: Optional[int] = 1000):
        query = f"SELECT * FROM {schema_name}.{table_name}\n"
        if limit is not None:
            query += f"LIMIT {limit}"
        return driver.query(query)
        
    globals()[f"api_route_{model.__name__}"] = func()
