import logging
import os

from typing import List, Optional, Union
from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.logger import logger

from util import ModelEndpointFactory, SQLAlchemyDriver

DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")

app = FastAPI(debug=True)

uvicorn_logger = logging.getLogger('uvicorn.error')
if __name__ != "main":
    logger.setLevel(uvicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

driver = SQLAlchemyDriver(DB_CONNECTION_STRING)

routers = []

for config in ModelEndpointFactory(DB_CONNECTION_STRING).generate_endpoint_configs():
    
    route = config.route

    router = APIRouter(prefix=route)
    
    pydantic_model = config.pydantic_model
    
    @router.get("/", response_model=Union[List[pydantic_model], pydantic_model])
    def func(request:Request,limit: Optional[int] = 10):
        schema_name, table_name = request.url.path.strip("/").split("/")[-2:]
        logger.info("TEST")
        query = f"SELECT * FROM {schema_name}.{table_name}\n"
        if limit is not None:
            query += f"LIMIT {limit}"
        return driver.query(query)
    routers.append(router)
    
@app.get("/health")
@app.get("/health/")
def healthcheck():
    return Response(status_code=200)

for router in routers:
    app.include_router(router)
