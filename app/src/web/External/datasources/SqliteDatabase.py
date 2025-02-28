from src.web.pkg.interfaces.externalInterfaces import DataBaseExternalInterface


class SqliteDatabase(DataBaseExternalInterface):
    def __init__(self,
                 conn):
        
        self._conn = conn
        self._cursor = conn.cursor()
        
    def get(self, id, table,  withDeleted=True) -> str:
        if withDeleted:
            query = f"SELECT * FROM {table} WHERE id = {id}"
        else:
            query = f"SELECT * FROM {table} WHERE id = {id} AND deleted_at IS NULL"
            
        self._cursor.execute(query)
        data = self._cursor.fetchall()
        if len(data) == 0:
            return None
        return data[0]
    
    def getAll(self, table, withDeleted=True) -> str:
        if withDeleted:
            query = f"SELECT * FROM {table}"
        else:
            query = f"SELECT * FROM {table} WHERE deleted_at IS NULL"
            
        self._cursor.execute(query)
        data = self._cursor.fetchall()
        if len(data) == 0:
            return None
        return data
    
    def create(self, data, table) -> str:
        
        columns = ', '.join(data.keys())  # Pega os nomes das colunas
        placeholders = ', '.join(['?'] * len(data))  # Cria os placeholders
        values = tuple(data.values())  # Pega os valores

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        self._cursor.execute(query, values)
        self._conn.commit()
        return self._cursor.lastrowid
    
    
    def update(self, id, data, table) -> str:
        
        columns = ', '.join([f"{col} = ?" for col in data.keys()])  # Associa cada coluna ao valor
        placeholders = ', '.join(['?'] * len(data))  # Cria os placeholders para as colunas
        values = tuple(data.values())  # Pega os valores

        query = f"UPDATE {table} SET {columns} WHERE id = {id}"
        self._cursor.execute(query, values)
        self._conn.commit()
        return self._cursor.lastrowid

    def delete(self, id, table) -> str:
        
        query = f"DELETE FROM {table} WHERE id = {id}"
        
        self._cursor.execute(query)
        self._conn.commit()
        return self._cursor.lastrowid
    
    def softDelete(self, id, table) -> str:
        
        query = f"UPDATE {table} SET deleted_at = CURRENT_TIMESTAMP WHERE id = {id}"
        
        self._cursor.execute(query)
        self._conn.commit()
        return self._cursor.lastrowid
    
        
    