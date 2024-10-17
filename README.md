FarmTech Solutions - Modelagem de Banco de Dados

## 📋 Sumário
- [Introdução](#introdução)
- [Objetivos](#objetivos)
- [Entidades e Atributos](#entidades-e-atributos)
- [Relacionamentos](#relacionamentos)
- [Cardinalidade](#cardinalidade)
- [Diagrama Entidade-Relacionamento (DER)](#diagrama-entidade-relacionamento-der)
- [Scripts SQL](#scripts-sql)
- [Implementação no SQLAlchemy](#implementação-no-sqlalchemy)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Como Usar](#como-usar)
- [Testes](#testes)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Referências](#referências)
- [Informações do Entregável](#informações-do-entregável)

## Introdução
Este projeto visa a modelagem de um banco de dados para a **FarmTech Solutions**, uma startup focada na Agricultura Digital. O sistema permitirá o monitoramento e gerenciamento de dados coletados por sensores em plantações agrícolas, facilitando a tomada de decisões baseada em dados.

## Objetivos
- Desenvolver uma modelagem de banco de dados eficiente e escalável.
- Implementar relacionamentos que reflitam as necessidades do negócio.
- Integrar o banco de dados com uma aplicação Python usando SQLAlchemy.
- Documentar todas as etapas e componentes do projeto.

## Entidades e Atributos
### 1. Produtor
- **id_produtor** (PK) - INTEGER, AUTOINCREMENT, NOT NULL
- **nome** - VARCHAR(100), NOT NULL
- **email** - VARCHAR(100), NOT NULL
- **telefone** - VARCHAR(20), NULL

### 2. Cultura
- **id_cultura** (PK) - INTEGER, AUTOINCREMENT, NOT NULL
- **tipo_cultura** - VARCHAR(100), NOT NULL
- **data_plantio** - DATE, NOT NULL
- **data_colheita** - DATE, NULL
- **id_produtor** (FK) - INTEGER, NOT NULL

### 3. Sensor
- **id_sensor** (PK) - INTEGER, AUTOINCREMENT, NOT NULL
- **tipo_sensor** - ENUM('S1', 'S2', 'S3'), NOT NULL
- **localizacao** - VARCHAR(100), NOT NULL
- **data_instalacao** - DATE, NOT NULL
- **id_cultura** (FK) - INTEGER, NOT NULL

### 4. Leitura
- **id_leitura** (PK) - INTEGER, AUTOINCREMENT, NOT NULL
- **data_hora** - DATETIME, NOT NULL
- **valor_umidade** - DOUBLE, NULL
- **valor_pH** - DOUBLE, NULL
- **valor_P** - DOUBLE, NULL
- **valor_K** - DOUBLE, NULL
- **valor_N** - DOUBLE, NULL
- **valor_temp_solo** - DOUBLE, NULL
- **id_sensor** (FK) - INTEGER, NOT NULL

### 5. AjusteIrrigacao
- **id_ajuste_irrigacao** (PK) - INTEGER, AUTOINCREMENT, NOT NULL
- **data_hora** - DATETIME, NOT NULL
- **quantidade_agua** - DOUBLE, NOT NULL
- **id_cultura** (FK) - INTEGER, NOT NULL

### 6. AjusteNutrientes
- **id_ajuste_nutrientes** (PK) - INTEGER, AUTOINCREMENT, NOT NULL
- **data_hora** - DATETIME, NOT NULL
- **quantidade_P** - DOUBLE, NOT NULL
- **quantidade_K** - DOUBLE, NOT NULL
- **quantidade_N** - DOUBLE, NOT NULL
- **id_cultura** (FK) - INTEGER, NOT NULL

## Relacionamentos
- **Produtor** possui **Cultura** (1:N)
- **Cultura** possui **Sensor** (1:N)
- **Sensor** possui **Leitura** (1:N)
- **Cultura** possui **AjusteIrrigacao** (1:N)
- **Cultura** possui **AjusteNutrientes** (1:N)

## Cardinalidade
Cada relacionamento foi definido com base nas regras de negócio, garantindo que a modelagem atenda às necessidades do sistema. A cardinalidade mínima e máxima foi estabelecida para cada relacionamento conforme discutido nas aulas.

## Diagrama Entidade-Relacionamento (DER)
![Diagrama ER](./imagens/farmtech_der.png)

## Scripts SQL
Os scripts SQL para criação das tabelas e definição das relações estão disponíveis na pasta [scripts](./scripts/farmtech_schema.sql).

## Implementação no SQLAlchemy
O banco de dados foi implementado utilizando **SQLAlchemy** em Python. A estrutura completa está disponível no arquivo `modelo.py` na pasta [modelos](./modelos/).

### Exemplo de Implementação:
```python
# modelos/modelo.py

from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Produtor(Base):
    __tablename__ = 'produtores'
    
    id_produtor = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    telefone = Column(String(20))
    
    culturas = relationship('Cultura', back_populates='produtor')

class Cultura(Base):
    __tablename__ = 'culturas'
    
    id_cultura = Column(Integer, primary_key=True, autoincrement=True)
    tipo_cultura = Column(String(100), nullable=False)
    data_plantio = Column(Date, nullable=False)
    data_colheita = Column(Date)
    id_produtor = Column(Integer, ForeignKey('produtores.id_produtor'), nullable=False)
    
    produtor = relationship('Produtor', back_populates='culturas')
    sensores = relationship('Sensor', back_populates='cultura')
    ajustes_irrigacao = relationship('AjusteIrrigacao', back_populates='cultura')
    ajustes_nutrientes = relationship('AjusteNutrientes', back_populates='cultura')

class Sensor(Base):
    __tablename__ = 'sensores'
    
    id_sensor = Column(Integer, primary_key=True, autoincrement=True)
    tipo_sensor = Column(Enum('S1', 'S2', 'S3', name='tipo_sensor_enum'), nullable=False)
    localizacao = Column(String(100), nullable=False)
    data_instalacao = Column(Date, nullable=False)
    id_cultura = Column(Integer, ForeignKey('culturas.id_cultura'), nullable=False)
    
    cultura = relationship('Cultura', back_populates='sensores')
    leituras = relationship('Leitura', back_populates='sensor')

class Leitura(Base):
    __tablename__ = 'leituras'
    
    id_leitura = Column(Integer, primary_key=True, autoincrement=True)
    data_hora = Column(DateTime, nullable=False)
    valor_umidade = Column(Float)  # Substituir por DOUBLE se necessário
    valor_pH = Column(Float)       # Substituir por DOUBLE
    valor_P = Column(Float)        # Substituir por DOUBLE
    valor_K = Column(Float)        # Substituir por DOUBLE
    valor_N = Column(Float)        # Substituir por DOUBLE
    valor_temp_solo = Column(Float)  # Substituir por DOUBLE, opcional
    id_sensor = Column(Integer, ForeignKey('sensores.id_sensor'), nullable=False)
    
    sensor = relationship('Sensor', back_populates='leituras')

class AjusteIrrigacao(Base):
    __tablename__ = 'ajustes_irrigacao'
    
    id_ajuste_irrigacao = Column(Integer, primary_key=True, autoincrement=True)
    data_hora = Column(DateTime, nullable=False)
    quantidade_agua = Column(Float, nullable=False)  # Substituir por DOUBLE
    id_cultura = Column(Integer, ForeignKey('culturas.id_cultura'), nullable=False)
    
    cultura = relationship('Cultura', back_populates='ajustes_irrigacao')

class AjusteNutrientes(Base):
    __tablename__ = 'ajustes_nutrientes'
    
    id_ajuste_nutrientes = Column(Integer, primary_key=True, autoincrement=True)
    data_hora = Column(DateTime, nullable=False)
    quantidade_P = Column(Float, nullable=False)  # Substituir por DOUBLE
    quantidade_K = Column(Float, nullable=False)  # Substituir por DOUBLE
    quantidade_N = Column(Float, nullable=False)  # Substituir por DOUBLE
    id_cultura = Column(Integer, ForeignKey('culturas.id_cultura'), nullable=False)
    
    cultura = relationship('Cultura', back_populates='ajustes_nutrientes')

# Configuração do banco de dados
engine = create_engine('sqlite:///farmtech.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
