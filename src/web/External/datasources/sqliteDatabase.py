from src.web.pkg.interfaces.externalInterfaces import DataBaseExternalInterface


class sqliteDatabase(DataBaseExternalInterface):
    def __init__(self,
                 cursor):
        
        self._cursor = cursor
        
    def get(self, id, table) -> str:
        self._cursor.execute("SELECT * FROM ? WHERE id = ?", (table, id, ))
        data = self._cursor.fetchall()
        return data
    
    def getAll(self, table) -> str:
        self._cursor.execute("SELECT * FROM ?", (table, ))
        data = self._cursor.fetchall()
        return data
    
    def create(self, data, table) -> str:
        
        columns = ', '.join(data.keys())  # Pega os nomes das colunas
        placeholders = ', '.join(['?'] * len(data))  # Cria os placeholders
        values = tuple(data.values())  # Pega os valores

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        self._cursor.execute(query, values)
        self.conn.commit()
        return self._cursor.lastrowid
    
    
    def update(self, id, data, table) -> str:
        
        columns = ', '.join(data.keys())  # Pega os nomes das colunas
        placeholders = ', '.join(['?'] * len(data))  # Cria os placeholders
        values = tuple(data.values())  # Pega os valores
        
        query = f"UPDATE {table} SET {columns} = {placeholders} WHERE id = {id}"
        
        self._cursor.execute(query, values)
        self.conn.commit()
        return self._cursor.lastrowid

    def delete(self, id, table) -> str:
        
        query = f"DELETE FROM {table} WHERE id = {id}"
        
        self._cursor.execute(query)
        self.conn.commit()
        return self._cursor.lastrowid
    
        
    