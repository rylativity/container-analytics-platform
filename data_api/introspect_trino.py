import logging
from typing import List, Dict, Optional

from pydantic import BaseModel, create_model

from pyhive import trino

class ModelEndpointFactory:

    log = logging.getLogger(__name__)
    log.setLevel("INFO")

    def __init__(self, trino_host:str = 'localhost'):
        self.trino_host = trino_host
        self.get_conn()

    def get_conn(self):
        self.conn = trino.connect(self.trino_host)
    
    def get_cursor(self):
        if not self.conn:
            self.get_conn()
        return self.conn.cursor()

    def get_schemas(self, exclude: List[str] = None) -> List[str]:
        
        query_string = "SHOW SCHEMAS"
        cursor = self.get_cursor()
        cursor.execute(query_string) 
        schemas = [row[0] for row in cursor.fetchall()]
        if exclude is not None:
            schemas = [s for s in schemas if s not in exclude]
        return schemas

    def get_tables_in_schema(self, schema: str, exclude: List[str] = None) -> List[str]:
        
        query_string = f"SHOW TABLES IN {schema}"
        cursor = self.get_cursor()
        cursor.execute(query_string) 
        tables = [row[0] for row in cursor.fetchall()]
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
        cursor = self.get_cursor()
        cursor.execute(query_string)
        res = cursor.fetchall()
        col_names = [row[0] for row in res]
        col_types = [type_mapper[row[1]] for row in res]
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

