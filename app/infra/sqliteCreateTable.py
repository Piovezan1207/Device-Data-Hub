import sqlite3

# Conectar ao banco
try:
    conn = sqlite3.connect("app/infra/database/banco.db")
except:
    conn = sqlite3.connect("infra/database/banco.db")
    
cursor = conn.cursor()
print("Iniciando a criação do banco...")
# Criar tabelas
cursor.executescript("""
CREATE TABLE IF NOT EXISTS robots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    axis INTEGER NOT NULL,
    brand TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS brokers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT NOT NULL,
    port INTEGER NOT NULL,
    user TEXT ,
    password TEXT, 
    nickname TEXT,
    deleted_at datetime DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    robot_id INTEGER NOT NULL,
    broker_id INTEGER NOT NULL,
    topic TEXT NOT NULL,
    ip TEXT NOT NULL CHECK (LENGTH(ip) <= 15),
    port INTEGER NOT NULL,
    description TEXT,
    token TEXT,
    FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE
    FOREIGN KEY (broker_id) REFERENCES brokers(id) ON DELETE CASCADE
);
""")

# Salvar e fechar conexão
conn.commit()

robots = [
    ('HC10', 6, 'YASKAWA'),
    ('GP8', 6, 'YASKAWA'),
    ('MIR100', 3, 'MIR'),
    ('KR 20-3', 6, 'KUKA'),
    ('TX2-60', 6, 'STAUBLI'),
]

# Inserir dados na tabela
cursor.executemany("INSERT INTO robots (type, axis, brand) VALUES (?, ?, ?)", robots)

conn.commit()
conn.close()
