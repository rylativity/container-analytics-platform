from fastapi import FastAPI
import json

from introspect_trino import TRINO_ROUTES_AND_MODELS

app = FastAPI(debug=True)

for route, model in TRINO_ROUTES_AND_MODELS.items():
    
    @app.get(route, response_model=model)
    def func():
        return f"Created route at {route} for model {model.__name__}"
    globals()[f"api_route_{model.__name__}"] = func()
