from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Robot(Base):
    __tablename__ = "robots"

    id = Column(Integer, primary_key=True)
    type = Column(String(128), nullable=False)
    axis = Column(Integer, nullable=False)
    brand = Column(String(128), nullable=False)

    # Relacionamento com a tabela de conexões
    connections = relationship("Connection", back_populates="robot", cascade="all, delete-orphan")

class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True)
    robot_id = Column(Integer, ForeignKey("robots.id", ondelete="CASCADE"), nullable=False)
    topic = Column(String(128), nullable=False)
    ip = Column(String(15), nullable=False)
    port = Column(Integer, nullable=False)
    description = Column(String(256), nullable=True)
    # number = Column(String(64), nullable=True)
    password = Column(String(128), nullable=True)

    # Relacionamento com a tabela de robôs
    robot = relationship("Robot", back_populates="connections")