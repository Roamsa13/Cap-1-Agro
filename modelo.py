# modelo.py

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# Criação da base declarativa
Base = declarative_base()

# Definição das Entidades

class Produtor(Base):
    __tablename__ = 'produtores'
    
    id_produtor = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    telefone = Column(String(20))
    
    # Relacionamento com Cultura
    culturas = relationship('Cultura', back_populates='produtor', cascade="all, delete-orphan")

class Cultura(Base):
    __tablename__ = 'culturas'
    
    id_cultura = Column(Integer, primary_key=True, autoincrement=True)
    tipo_cultura = Column(String(50), nullable=False)
    data_plantio = Column(Date, nullable=False)
    data_colheita = Column(Date)
    id_produtor = Column(Integer, ForeignKey('produtores.id_produtor'), nullable=False)
    
    # Relacionamentos
    produtor = relationship('Produtor', back_populates='culturas')
    sensores = relationship('Sensor', back_populates='cultura', cascade="all, delete-orphan")
    ajustes_irrigacao = relationship('AjusteIrrigacao', back_populates='cultura', cascade="all, delete-orphan")
    ajustes_nutrientes = relationship('AjusteNutrientes', back_populates='cultura', cascade="all, delete-orphan")

class Sensor(Base):
    __tablename__ = 'sensores'
    
    id_sensor = Column(Integer, primary_key=True, autoincrement=True)
    tipo_sensor = Column(Enum('S1', 'S2', 'S3', name='tipo_sensor'), nullable=False)
    localizacao = Column(String(100))
    data_instalacao = Column(Date)
    id_cultura = Column(Integer, ForeignKey('culturas.id_cultura'), nullable=False)
    
    # Relacionamentos
    cultura = relationship('Cultura', back_populates='sensores')
    leituras = relationship('Leitura', back_populates='sensor', cascade="all, delete-orphan")

class Leitura(Base):
    __tablename__ = 'leituras'
    
    id_leitura = Column(Integer, primary_key=True, autoincrement=True)
    data_hora = Column(DateTime, nullable=False)
    valor_pH = Column(Float)
    valor_P = Column(Float)
    valor_K = Column(Float)
    valor_umidade = Column(Float)
    id_sensor = Column(Integer, ForeignKey('sensores.id_sensor'), nullable=False)
    
    # Relacionamentos
    sensor = relationship('Sensor', back_populates='leituras')

class AjusteIrrigacao(Base):
    __tablename__ = 'ajustes_irrigacao'
    
    id_ajuste = Column(Integer, primary_key=True, autoincrement=True)
    data_hora = Column(DateTime, nullable=False)
    quantidade_agua = Column(Float, nullable=False)
    id_cultura = Column(Integer, ForeignKey('culturas.id_cultura'), nullable=False)
    
    # Relacionamentos
    cultura = relationship('Cultura', back_populates='ajustes_irrigacao')

class AjusteNutrientes(Base):
    __tablename__ = 'ajustes_nutrientes'
    
    id_ajuste = Column(Integer, primary_key=True, autoincrement=True)
    data_hora = Column(DateTime, nullable=False)
    quantidade_P = Column(Float, nullable=False)
    quantidade_K = Column(Float, nullable=False)
    id_cultura = Column(Integer, ForeignKey('culturas.id_cultura'), nullable=False)
    
    # Relacionamentos
    cultura = relationship('Cultura', back_populates='ajustes_nutrientes')

# Configuração do banco de dados
def get_engine(db_url='sqlite:///farmtech.db'):
    """
    Cria e retorna o motor do SQLAlchemy.

    Args:
        db_url (str): URL de conexão com o banco de dados.

    Returns:
        Engine: Motor do SQLAlchemy.
    """
    return create_engine(db_url, echo=False, future=True)

# Criação das tabelas
def create_tables(engine):
    """
    Cria todas as tabelas definidas na base declarativa.

    Args:
        engine (Engine): Motor do SQLAlchemy.
    """
    Base.metadata.create_all(engine)

# Configuração da sessão
def get_session(engine):
    """
    Cria e retorna uma sessão do SQLAlchemy.

    Args:
        engine (Engine): Motor do SQLAlchemy.

    Returns:
        Session: Sessão do SQLAlchemy.
    """
    Session = sessionmaker(bind=engine, expire_on_commit=False, future=True)
    return Session()

# Inicialização do banco de dados e sessão
engine = get_engine()
create_tables(engine)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)
session = SessionLocal()