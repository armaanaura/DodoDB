from typing import Any, List

class Column:
    def __init__(self, column_name:str, column_dtype: Any):
        valid_types = (int, str, float, bool)
        
        if column_dtype not in valid_types:
            raise ValueError(f"Invalid datatype {column_dtype}. Valid types are: {valid_types}")
        
        self.name = column_name
        self.dtype = column_dtype
    
    def change_name(self,new_name:str):
        self.name = new_name

class Table:
    def __init__(self, table_name:str):
        self.name = table_name
        self.columns: dict[str, Column] = {}
        self.rows: List[dict[str,Any]] = []
        
    
    def list_columns(self, detailed:bool=False):
        column_number:int = 0
        for column in self.columns.values():
            if detailed:
                print(column_number,"    ",column.name,"    ",str(column.dtype))            
            else:
                print(column_number,"    ",column.name)
            column_number += 1
    
    def create_column(self, column_name: str, column_dtype: Any):
        column = Column(column_name, column_dtype)
        self.columns[column_name] = column
        return column
    
    def add_row(self, row_content: dict[str, Any]):
        for column_name_entry in row_content.keys():
            if self.columns.__contains__(column_name_entry) == False:
                raise ValueError(f"Column with column name {column_name_entry} doesn't exist")
            
        self.rows.append(row_content)
            
            
class Database:
    def __init__(self, database_name:str, metadata:str=""):
        self.name = database_name
        self.metadata: str = metadata
        self.tables: dict[str, Table] = {}
        
    def create_table(self, table_name:str) -> Table:
        table = Table(table_name)
        if self.tables.__contains__(table_name):
            raise ValueError(f"Table with name {table_name} already exists in database {self.name}")
        else:
            self.tables[table_name] = table
        
        return table
            
    def list_tables(self, detailed:bool=False):
        table_number:int = 0
        for table in self.tables.values():
            if detailed:
                print(table_number,"    ",table.name,"    ",str(len(table.columns))+" columns")            
            else:
                print(table_number,"    ",table.name)
            table_number += 1
    
    def get_table(self, table_name:str) -> Table:
        if self.tables.__contains__(table_name):
            return self.tables[table_name]
        else:
            raise ValueError(f"Table with name {table_name} does not exist in database {self.name}")