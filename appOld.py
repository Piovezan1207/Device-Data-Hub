from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import Robot, Connection

import threading

import time

from mqttThread import startMqttThread

mqttThread, mqttClient = None, None

from threadGeneratorTest import createRobotThread

robotThreadList = {}

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Robot, Connection, Base

  


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'  # Use SQLite como exemplo
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)



# def startAllThreads():

# time.sleep(5)


#DESCOMENTAR DEPOIS QUE TERMONAR O HTML

mqttThread, mqttClient = startMqttThread()

# Configuração do banco de dados
engine = create_engine('sqlite:///instance/banco.db')  # Ou o banco que você estiver usando
Base.metadata.create_all(engine)  # Cria as tabelas
Session = sessionmaker(bind=engine)
session = Session()
connections = session.query(Connection).all()
for connection in connections:
    if not connection.id in robotThreadList:
        robotThreadList[connection.id] = createRobotThread(connection, session.query(Robot).filter(Robot.id == connection.robot_id).first(), mqttClient)
        # robotThreadList[connection.id].start()
session.close()  


    
@app.cli.command("seed")
def seed():
    """Popula o banco de dados com dados iniciais."""
    robots = [
        Robot(type="MIR100", axis=3, brand="MIR"),
        Robot(type="HC10", axis=6, brand="WASKAWA")
    ]

    db.session.add_all(robots)
    db.session.commit()
    print("Seed data inserted!")

@app.route('/connection')
def connection():
    robots = db.session.query(Robot).all()  # Obtém todos os robôs
    robots_list = []
    for robot in robots:
        robots_list.append({
            'id': robot.id,
            'type': robot.type,
            'axis': robot.axis,
            'brand': robot.brand
        })
    
    return render_template('/connections/index.html', robots=robots_list)

@app.route('/connection', methods=['POST'])
def connectionPost():
    print(request.form.get('robotIp'),
          request.form.get('robotPort'),
          request.form.get('robotDescription'),
          request.form.get('robotPassword'),
          request.form.get('robotMqttTopic'))
    return redirect('/')

@app.route('/')
def home():
    
    robots = db.session.query(Robot).all()  # Obtém todos os robôs
    robots_list = {}
    for robot in robots:
        robots_list[robot.id]  = {
            'id': robot.id,
            'type': robot.type,
            'axis': robot.axis,
            'brand': robot.brand
        }
        
    print(robots_list)
    
    connections = db.session.query(Connection).all()
    connections_list = []
    for connection in connections:
        connections_list.append({
            'id': connection.id,
            'robot_id': robots_list[connection.robot_id],
            'ip': connection.ip,
            'port': connection.port,
            'description': connection.description,
            # 'number': connection.number,
            'token': connection.token,
            'topic': connection.topic
        })
    
    return render_template("/home/index.html",  connections=connections_list)
    # return "Servidor Flask está rodando!"

@app.route('/robots', methods=['GET'])
def get_robots():
    robots = db.session.query(Robot).all()  # Obtém todos os robôs
    robots_list = []
    for robot in robots:
        robots_list.append({
            'id': robot.id,
            'type': robot.type,
            'axis': robot.axis,
            'brand': robot.brand
        })

    return jsonify(robots_list)

@app.route('/robot/<int:id>', methods=['GET'])
def get_robot(id):
    robot = db.session.query(Robot).filter(Robot.id == id).first()  # Obtém um robô pelo ID
    if robot:
        return jsonify({
            'id': robot.id,
            'type': robot.type,
            'axis': robot.axis,
            'brand': robot.brand
        })
    return jsonify({'error': 'Robot not found'}), 404

@app.route('/connections', methods=['GET'])
def get_connections():
    connections = db.session.query(Connection).all()
    connections_list = []
    for connection in connections:
        connections_list.append({
            'id': connection.id,
            'robot_id': connection.robot_id,
            'ip': connection.ip,
            'port': connection.port,
            'description': connection.description,
            # 'number': connection.number,
            'token': connection.token,
            'topic': connection.topic
        })
        
    return jsonify(connections_list)

@app.route('/connection/<int:id>', methods=['GET'])
def get_connection(id):
    connection = db.session.query(Connection).filter(Connection.id == id).first()
    if connection:
        return jsonify({
            'id': connection.id,
            'robot_id': connection.robot_id,
            'ip': connection.ip,
            'port': connection.port,
            'description': connection.description,
            # 'number': connection.number,
            'token': connection.token,
            'topic': connection.topic
        })
    return jsonify({'error': 'Connection not found'}), 404

@app.route('/connection', methods=['POST'])
def create_connection():
    data = request.json
    connection = Connection(robot_id=data['robot_id'], ip=data['ip'], port=data['port'], topic=data['topic'], description=data['description'], number=data['number'], token=data['token'])
    db.session.add(connection)
    db.session.commit()
   
    robotThreadList[connection.id] = createRobotThread(connection, db.session.query(Robot).filter(Robot.id == data['robot_id']).first(), mqttClient)    
    robotThreadList[connection.id].start()
    return jsonify({'message': 'Connection created successfully!'})

@app.route('/connection/<int:id>', methods=["DELETE"])
def delete_connection(id):
    robotThreadList[id].stop()
    robotThreadList[id].join()
    robotThreadList.pop(id)
    
    connection = db.session.query(Connection).filter(Connection.id == id).first()
    if connection:
        db.session.delete(connection)
        db.session.commit()
        return jsonify({'message': 'Connection deleted successfully!'})
    return jsonify({'error': 'Connection not found'}), 404

if __name__ == '__main__':
    # thread = threading.Thread(target=startAllThreads, daemon=True)
    # thread.start()  # Inicia o script antes do Flask rodar
    # startAllThreads()
    app.run(debug=False)
