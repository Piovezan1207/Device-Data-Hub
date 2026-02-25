#!/bin/sh

DB_PATH="/app/infra/database/database.db"

# Verifica se o banco já existe
if [ ! -f "$DB_PATH" ]; then
    echo "Banco de dados não encontrado. Criando..."
    python /app/infra/sqliteCreateTable.py
    echo "Banco de dados criado!"
else
    echo "Banco de dados já existe."
fi

# Executa o comando passado ao container (exemplo: iniciar a aplicação)
exec "$@"
