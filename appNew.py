from flask import Flask, jsonify, request, render_template, redirect

from models import Robot, Connection

import sqlite3

from mqttThread import startMqttThread

mqttThread, mqttClient = None, None

from threadGeneratorTest import createRobotThread

robotThreadList = {}

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Robot, Connection, Base

######### External 
#Database
from src.web.External.datasources.SqliteDatabase import SqliteDatabase
#Connection with robots
from src.web.External.integrations.connectionExternal import connectionExternal, ThreadManager

######### Controller arch 
from src.web.adapters.controller.ConnectionController import ConnectionController
from src.web.adapters.controller.RobotController import RobotController


conn = sqlite3.connect("instance/banco.db", check_same_thread=False)
database = SqliteDatabase(conn)

manager = ThreadManager()
externalConnThreads = connectionExternal(manager)

app = Flask(__name__)

robots = RobotController.getAllRobots(database)
print(robots)

@app.route('/connection')
def connection():
    robots = RobotController.getAllRobots(database)
    print(robots)
    return render_template('/connections/index.html', robots=robots["robots"])

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
    
    robots = RobotController.getAllRobots(database)
        
    print(robots)
    
    connections = ConnectionController.getAllConnections(database, mqttClient, externalConnThreads)

    print(connections)
    return render_template("/home/index.html",  connections=connections["connections"], robots=robots)
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
            'number': connection.number,
            'password': connection.password,
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
            'number': connection.number,
            'password': connection.password,
            'topic': connection.topic
        })
    return jsonify({'error': 'Connection not found'}), 404

@app.route('/connection', methods=['POST'])
def create_connection():
    data = request.json
    connection = Connection(robot_id=data['robot_id'], ip=data['ip'], port=data['port'], topic=data['topic'], description=data['description'], number=data['number'], password=data['password'])
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
