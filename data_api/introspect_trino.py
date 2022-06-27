import logging
from typing import List, Dict, Optional

from pydantic import BaseModel, create_model

from sqlalchemy import create_engine

class SQLAlchemyDriver:

    def __init__(self, connection_string:str):
        self.engine = create_engine(connection_string)
    
    def query(self, query_string: str):
        with self.engine.connect() as conn:
            result = conn.execute(query_string)
        return [dict(row) for row in result]

class EndpointConfig:
    """ Simple Python object representing an endpoint configuration dynamically generated from a SQL table
    """

    def __init__(self, route:str, pydantic_model: BaseModel, sqlalchemy_model) -> None:
        pass

class ModelEndpointFactory:

    log = logging.getLogger(__name__)
    log.setLevel("INFO")

    def __init__(self, db_connection_string: str) -> None:
        self.driver = SQLAlchemyDriver(db_connection_string)

    def get_schemas(self, exclude: List[str] = None) -> List[str]:
        
        query_string = "SHOW SCHEMAS"
        res = self.driver.query(query_string=query_string)
        schemas = [row['Schema'] for row in res]
        if exclude is not None:
            schemas = [s for s in schemas if s not in exclude]
        return schemas

    def get_tables_in_schema(self, schema: str, exclude: List[str] = None) -> List[str]:
        
        query_string = f"SHOW TABLES IN {schema}"
        res = self.driver.query(query_string=query_string) 
        tables = [row['Table'] for row in res]
        if exclude is not None:
            tables = [t for t in tables if t not in exclude]
        return tables

    def get_cols_in_table(self, schema:str, table: str) -> dict:
        
        type_mapper = {
            'bigint':int,
            'timestamp(3)': str,
            'double': float,
            'varchar': str
        }
        
        query_string = f"DESC {schema}.{table}"
        res = self.driver.query(query_string=query_string)
        col_names = [row['Column'] for row in res]
        col_types = [type_mapper[row['Type']] for row in res]
        return dict(zip(col_names, col_types))

    def get_schema_structure(self, schema:str) -> dict:
        
        schema_structure = {}
        tables = self.get_tables_in_schema(schema=schema)
        for table in tables:
            schema_structure[table] = self.get_cols_in_table(schema=schema, table=table)
        return schema_structure

    def get_db_structure(self, exclude_schemas: List[str] = None) -> Dict[str, dict]:
        
        db_structure = {}
        schemas = self.get_schemas(exclude = exclude_schemas)
        for schema in schemas:
            db_structure[schema] = self.get_schema_structure(schema=schema)
        return db_structure

    def generate_api_routes_and_models(self, db_structure:Optional[Dict[str, dict]] = None) -> Dict[str, BaseModel]:
        routes_and_models = {}
        if db_structure is None:
            db_structure = self.get_db_structure(exclude_schemas=["information_schema"]).items()
        for schema, tables in db_structure:
            if tables:
                for table, cols in tables.items():
                    route = f"/{schema}/{table}"
                    model_name = schema[0].upper()+schema[1:].lower()+table[0].upper()+table[1:].lower()
                    # create_model expects fields to be tuples of the form (<type>, <default_val>)
                    # the dict_comprehension below formats the fields in the call to create_model
                    # wrapping in Optional[] and setting default of ... makes field nullable
                    model = create_model(model_name, **{k:(Optional[v],...) for k,v in cols.items()})
                    self.log.info(f"Created model for table {table} with schema\n {model.schema()}")
                    routes_and_models[route] = model
        return routes_and_models

if __name__ == "__main__":
    factory = ModelEndpointFactory(trino_host="localhost")
    routes_and_models = factory.generate_api_routes_and_models()

