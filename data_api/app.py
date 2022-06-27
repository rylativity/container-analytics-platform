import os

from typing import List, Optional, Union
from fastapi import FastAPI, Response

from introspect_trino import ModelEndpointFactory, SQLAlchemyDriver

DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")

app = FastAPI(debug=True)
driver = SQLAlchemyDriver(DB_CONNECTION_STRING)

for config in ModelEndpointFactory(DB_CONNECTION_STRING).generate_endpoint_configs():
    
    route = config.route
    schema_name, table_name = route.split("/")[-2:]

    pydantic_model = config.pydantic_model
    
    @app.get(route, response_model=Union[List[pydantic_model], pydantic_model])
    def func(limit: Optional[int] = 10):
        query = f"SELECT * FROM {schema_name}.{table_name}\n"
        if limit is not None:
            query += f"LIMIT {limit}"
        return driver.query(query)
        
    globals()[f"api_route_{pydantic_model.__name__}"] = func()

@app.get("/health")
@app.get("/health/")
def healthcheck():
    return Response(status_code=200)
