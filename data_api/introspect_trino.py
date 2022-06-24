from typing import List, Dict

from pydantic import create_model
from pydantic.main import ModelMetaclass

from pyhive import trino

#this is the docker service name
hostname = 'trino'

def get_conn(host:str):
    return trino.connect(host)
def get_cursor(host:str):
    return get_conn(host=host).cursor()

cursor = get_cursor(hostname)

def get_schemas(exclude: List[str] = None) -> List[str]:
    
    query_string = "SHOW SCHEMAS"
    cursor.execute(query_string) 
    schemas = [row[0] for row in cursor.fetchall()]
    if exclude is not None:
        schemas = [s for s in schemas if s not in exclude]
    return schemas

def get_tables_in_schema(schema: str, exclude: List[str] = None) -> List[str]:
    
    query_string = f"SHOW TABLES IN {schema}"
    cursor.execute(query_string) 
    tables = [row[0] for row in cursor.fetchall()]
    if exclude is not None:
        tables = [t for t in tables if t not in exclude]
    return tables

def get_cols_in_table(schema:str, table: str) -> dict:
    
    type_mapper = {
        'bigint':int,
        'timestamp(3)': str,
        'double': float,
        'varchar': str
    }
    
    query_string = f"DESC {schema}.{table}"
    cursor.execute(query_string)
    res = cursor.fetchall()
    col_names = [row[0] for row in res]
    col_types = [type_mapper[row[1]] for row in res]
    return dict(zip(col_names, col_types))

def get_schema_structure(schema:str) -> dict:
    
    schema_structure = {}
    tables = get_tables_in_schema(schema=schema)
    for table in tables:
        schema_structure[table] = get_cols_in_table(schema=schema, table=table)
    return schema_structure

def get_db_structure(exclude_schemas: List[str] = None) -> Dict[str, dict]:
    
    db_structure = {}
    schemas = get_schemas(exclude = exclude_schemas)
    for schema in schemas:
        db_structure[schema] = get_schema_structure(schema=schema)
    return db_structure

db_structure = get_db_structure(exclude_schemas=["information_schema"])

def generate_api_routes_and_models(db_structure:Dict[str, dict]):
    routes_and_models = {}
    for schema, tables in db_structure.items():
        if tables:
            for table, cols in tables.items():
                route = f"/{schema}/{table}"
                model_name = schema[0].upper()+schema[1:].lower()+table[0].upper()+table[1:].lower()
                model = create_model(model_name, **cols)
                routes_and_models[route] = model
    return routes_and_models

TRINO_ROUTES_AND_MODELS = generate_api_routes_and_models(db_structure=db_structure)
