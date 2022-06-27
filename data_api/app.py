import os

from typing import List, Optional, Union
from fastapi import FastAPI, Response

from introspect_trino import ModelEndpointFactory, SQLAlchemyDriver

DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")

app = FastAPI(debug=True)
driver = SQLAlchemyDriver(DB_CONNECTION_STRING)

for route, model in ModelEndpointFactory(DB_CONNECTION_STRING).generate_api_routes_and_models().items():

    schema_name, table_name = route.split("/")[-2:]
    
    @app.get(route, response_model=Union[List[model], model])
    def func(limit: Optional[int] = 10):
        query = f"SELECT * FROM {schema_name}.{table_name}\n"
        if limit is not None:
            query += f"LIMIT {limit}"
        return driver.query(query)
        
    globals()[f"api_route_{model.__name__}"] = func()

@app.get("/health")
@app.get("/health/")
def healthcheck():
    return Response(status_code=200)
