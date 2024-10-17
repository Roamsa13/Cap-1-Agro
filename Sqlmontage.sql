-- farmtech_schema.sql

CREATE TABLE produtores (
    id_produtor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20)
);

CREATE TABLE culturas (
    id_cultura INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_cultura VARCHAR(100) NOT NULL,
    data_plantio DATE NOT NULL,
    data_colheita DATE,
    id_produtor INTEGER NOT NULL,
    FOREIGN KEY (id_produtor) REFERENCES produtores(id_produtor)
);

CREATE TABLE sensores (
    id_sensor INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_sensor ENUM('S1', 'S2', 'S3') NOT NULL,
    localizacao VARCHAR(100) NOT NULL,
    data_instalacao DATE NOT NULL,
    id_cultura INTEGER NOT NULL,
    FOREIGN KEY (id_cultura) REFERENCES culturas(id_cultura)
);

CREATE TABLE leituras (
    id_leitura INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora DATETIME NOT NULL,
    valor_umidade DOUBLE,
    valor_pH DOUBLE,
    valor_P DOUBLE,
    valor_K DOUBLE,
    valor_N DOUBLE,
    valor_temp_solo DOUBLE,
    id_sensor INTEGER NOT NULL,
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor)
);

CREATE TABLE ajustes_irrigacao (
    id_ajuste_irrigacao INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora DATETIME NOT NULL,
    quantidade_agua DOUBLE NOT NULL,
    id_cultura INTEGER NOT NULL,
    FOREIGN KEY (id_cultura) REFERENCES culturas(id_cultura)
);

CREATE TABLE ajustes_nutrientes (
    id_ajuste_nutrientes INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora DATETIME NOT NULL,
    quantidade_P DOUBLE NOT NULL,
    quantidade_K DOUBLE NOT NULL,
    quantidade_N DOUBLE NOT NULL,
    id_cultura INTEGER NOT NULL,
    FOREIGN KEY (id_cultura) REFERENCES culturas(id_cultura)
);