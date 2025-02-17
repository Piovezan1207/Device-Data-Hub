import os

class Config:
    # Defina sua URL de conexão com o banco de dados (aqui usamos SQLite como exemplo)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///banco.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
