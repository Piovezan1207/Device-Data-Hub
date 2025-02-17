from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Robot, Connection, Base

# Configuração do banco de dados
engine = create_engine('sqlite:///banco.db')  # Ou o banco que você estiver usando
Base.metadata.create_all(engine)  # Cria as tabelas

Session = sessionmaker(bind=engine)
session = Session()

# Criando um robô e uma conexão
# robot = Robot(type='Industrial', axis=6, brand='XYZ Robotics')
# connection = Connection(
#     topic='robot/command',
#     ip='192.168.1.100',
#     port=502,
#     description='Main control connection',
#     number='001',
#     password='secret123',
#     robot=robot
# )

# session.add(robot)
# session.add(connection)
# session.commit()

# Consultar robôs e suas conexões
robots = session.query(Robot).all()
for robot in robots:
    print(f"Robot ID: {robot.id}, Type: {robot.type}, Brand: {robot.brand}")
    for conn in robot.connections:
        print(f"  Connection IP: {conn.ip}, Topic: {conn.topic}")

session.close()
