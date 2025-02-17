from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Use SQLite como exemplo
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Definição dos modelos
class Robot(db.Model):
    __tablename__ = 'robots'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    axis = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(128), nullable=False)


class Connection(db.Model):
    __tablename__ = 'connections'

    id = db.Column(db.Integer, primary_key=True)
    robot_id = db.Column(db.Integer, db.ForeignKey('robots.id'), nullable=False)
    topic = db.Column(db.String(128), nullable=False)
    ip = db.Column(db.String(15), nullable=False)  # Exemplo: IPv4
    port = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    number = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(128), nullable=True)

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

if __name__ == '__main__':
    app.run(debug=True)
