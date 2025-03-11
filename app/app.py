from flask import Flask, jsonify, request, render_template, redirect, flash, url_for
import sqlite3
import threading
import requests
import time
######### External 
#Database
from src.web.External.datasources.SqliteDatabase import SqliteDatabase
#Connection with robots
from src.web.External.integrations.connectionExternal import connectionExternal, ThreadManager

######### Controller arch 
from src.web.adapters.controller.ConnectionController import ConnectionController
from src.web.adapters.controller.RobotController import RobotController
from src.web.adapters.controller.BrokerController import BrokerController

conn = sqlite3.connect("infra/database/banco.db", check_same_thread=False)
database = SqliteDatabase(conn)

manager = ThreadManager()
externalConnThreads = connectionExternal(manager)

app = Flask(__name__)
app.secret_key = '123#Senai!!23@@()hd28'  # Required for flash messages
PORT=5000

def startup_task(run):
    time.sleep(10)
    print("Inicializando threads....")
    if run:
        requests.get(f'http://localhost:{PORT}/api/connection/start')

with app.app_context():
    threadStart = threading.Thread(target=startup_task, args=(True, ))  # Será executado quando o WSGI carregar o Flask
    threadStart.start()
    
@app.route('/broker/create')
def broker_create():
    return render_template('/brokers/create.html')

@app.route('/broker/create', methods=['POST'])
def broker_post():
    data = request.form.to_dict()    
    
    keysList = ['ip', 'port']
    
    for key in keysList:
        if key not in data or data[key] == '':
            flash('O campo {} é obrigatorio.'.format(key), 'error')  # Store error message
            return redirect(url_for('connection_create'))  # Redirect to the same page
    
    if 'user' not in data or data['user'] == '':
        data['user'] = ""
        
        
    if 'password' not in data or data['password'] == '':
        data['password'] = ""
        
    if 'nickname' not in data or data['nickname'] == '':
        data['nickname'] = ""
    
    # print(data)
    
    broker = BrokerController.createBroker(ip=data['ip'],
                                           port=int(data['port']),
                                           user=data['user'],
                                           password=data['password'],
                                            nickname=data['nickname'],  
                                           dataBaseExternal=database)
    
    flash('{} - Broker criado com sucesso!'.format(broker["id"]), 'succes')  # Store error message
    return redirect(url_for('brokers'))

@app.route('/broker')
def brokers():
    broker = BrokerController.getAllBrokers(database)
    return render_template('/brokers/index.html', brokers=broker["brokers"])

        

@app.route('/connection/create')
def connection_create():
    robots = RobotController.getAllRobots(database)
    brokers = BrokerController.getAllBrokers(database)
    return render_template('/connections/index.html', robots=robots["robots"], brokers=brokers["brokers"])

@app.route('/connection/create', methods=['POST'])
def connection_post():
    data = request.form.to_dict()    
    
    keysList = ['ip', 'port', 'description' , 'topic', 'robot_id', 'broker_id']
    
    for key in keysList:
        if key not in data or data[key] == '':
            flash('O campo {} é obrigatorio.'.format(key), 'error')  # Store error message
            return redirect(url_for('connection_create'))  # Redirect to the same page
        
    if 'token' not in data or data['token'] == '':
        data['token'] = ""
    
    
    connection = ConnectionController.createConnection(ip=data['ip'], 
                                                            port=int(data['port']),
                                                            description=data['description'],
                                                            token=data['token'],
                                                            mqttTopic=data['topic'],
                                                            robotId=data['robot_id'],
                                                            brokerId=data['broker_id'],
                                                            dataBaseExternal=database,
                                                            connectionExternal=externalConnThreads,
                                                            runConnection=True)
    
    flash('{} - Conexão com o robô {} criada com sucesso!'.format(connection["id"], connection["robot"]["type"]), 'succes')  # Store error message
    return redirect('/')


@app.route('/connection/update/<int:id>')
def connection_update(id):
    connection = ConnectionController.getConnection(id, database, externalConnThreads)
    robots = RobotController.getAllRobots(database)
    brokers = BrokerController.getAllBrokers(database)
    return render_template('/connections/update.html', connection=connection, robots=robots["robots"], brokers=brokers["brokers"])

@app.route('/connection/update/<int:id>', methods=['POST'])
def connection_update_post(id):
    data = request.form.to_dict()
    # print(data)
    
    keysList = ['ip', 'port', 'description',  'topic', 'robot_id', 'broker_id']
    
    for key in keysList:
        if key not in data or data[key] == '':
            flash('O campo {} é obrigatorio.'.format(key), 'error')  # Store error message
            return redirect(url_for('connection_update', id=id))  # Redirect to the same page
        
    if 'token' not in data or data['token'] == '':
        data['token'] = ""
    
    
    connection = ConnectionController.updateConnection(id = id,
                                                       ip=data['ip'], 
                                                        port=int(data['port']),
                                                        description=data['description'],
                                                        token=data['token'],
                                                        mqttTopic=data['topic'],
                                                        robotId=data['robot_id'],
                                                        brokerId=data['broker_id'],
                                                        dataBaseExternal=database,
                                                        connectionExternal=externalConnThreads,
                                                        runConnection=True)
    
    flash('{} - Conexão atualizada com sucesso.'.format(connection["id"]), 'succes')  # Store error message
    return redirect('/')



@app.route('/robots')
def robots():
    robots = RobotController.getAllRobots(database)
    return render_template('/robots/index.html', robots=robots["robots"])

@app.route('/')
def home():
    connections = ConnectionController.getAllConnections(database, externalConnThreads)
    print(externalConnThreads)
    return render_template("/home/index.html",  connections=connections["connections"])

########################################################################################################################################

@app.route('/api/robots', methods=['GET'])
def api_get_robots():
    robots = RobotController.getAllRobots(database)
    return jsonify(robots)

@app.route('/api/robot/<int:id>', methods=['GET'])
def api_get_robot(id):
   
    robot = RobotController.getRobot(id, database)
    return jsonify(robot)

@app.route('/api/broker/<int:id>', methods=["DELETE"])
def api_delete_broker(id):
   broker = BrokerController.deleteBroker(id, database)
   return jsonify(broker) 

@app.route('/api/connections', methods=['GET'])
def api_get_connections():
    connections = ConnectionController.getAllConnections(database, externalConnThreads)
    return jsonify(connections)

@app.route('/api/connection/<int:id>', methods=['GET'])
def api_get_connection(id):
    connections = ConnectionController.getConnection(id, database, externalConnThreads)
    return jsonify(connections)

@app.route('/api/connection', methods=['POST'])
def api_create_connection():
    data = request.json
    
    keysList = ['ip', 'port', 'description', 'token', 'topic', 'robot_id', 'broker_id']
    
    for key in keysList:
        if key not in data:
            return jsonify({"error": "Missing key {}".format(key)})
    
    connection = ConnectionController.createConnection(ip=data['ip'], 
                                                            port=data['port'],
                                                            description=data['description'],
                                                            token=data['token'],
                                                            mqttTopic=data['topic'],
                                                            robotId=data['robot_id'],
                                                            brokerId=data['broker_id'],
                                                            dataBaseExternal=database,
                                                            connectionExternal=externalConnThreads,
                                                            runConnection=False)
   
    return jsonify(connection)

@app.route('/api/connection/<int:id>', methods=["PUT"])
def api_update_connection(id):
    data = request.json

    keysList = ['ip', 'port', 'description', 'token', 'topic', 'robot_id', 'broker_id']

    for key in keysList:
        if key not in data:
            return jsonify({"error": "Missing key {}".format(key)})

    connection = ConnectionController.updateConnection( id = id,
                                                        ip=data['ip'], 
                                                        port=data['port'],
                                                        description=data['description'],
                                                        token=data['token'],
                                                        mqttTopic=data['topic'],
                                                        robotId=data['robot_id'],
                                                        brokerId=data['broker_id'],
                                                        dataBaseExternal=database,
                                                        connectionExternal=externalConnThreads,
                                                        runConnection=False)
    
    return jsonify(connection) 

@app.route('/api/connection/<int:id>', methods=["DELETE"])
def api_delete_connection(id):
   connection = ConnectionController.deleteConnection(id, database, externalConnThreads)
   return jsonify(connection) 

@app.route('/api/connection/start/<int:id>', methods=["GET"])
def api_start_connection(id):
   connection = ConnectionController.runConnection(id, database, externalConnThreads)
   return jsonify(connection) 

@app.route('/api/connection/stop/<int:id>', methods=["GET"])
def api_stop_connection(id):
   connection = ConnectionController.stopConnection(id, database, externalConnThreads)
   return jsonify(connection) 

@app.route('/api/connection/start', methods=["GET"])
def api_start_all_connection():
   connection = ConnectionController.runAllConnections(database, externalConnThreads)
   return jsonify(connection) 

   

if __name__ == '__main__':
    # ConnectionController.runAllConnections(database, externalConnThreads)
    app.run(debug=True, host="0.0.0.0", port=PORT)
