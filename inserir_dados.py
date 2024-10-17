import sqlite3

def conectar():
    """
    Conecta ao banco de dados SQLite.
    Se o arquivo do banco de dados não existir, ele será criado.
    """
    DATABASE_URL = '/Applications/DB Browser for SQLite.app/Contents/MacOS/DB Browser for SQLite.db'
    
    try:
        connection = sqlite3.connect(DATABASE_URL)
        print("Conexão estabelecida com sucesso!")
        return connection
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabela(connection):
    """
    Cria uma tabela chamada 'produtos' no banco de dados.
    """
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL
            )
        ''')
        print("Tabela 'produtos' criada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        cursor.close()

def inserir_produto(connection, nome, preco):
    """
    Insere um novo produto na tabela 'produtos'.
    """
    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, preco)
            VALUES (?, ?)
        ''', (nome, preco))
        connection.commit()
        print(f"Produto '{nome}' inserido com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inserir produto: {e}")
    finally:
        cursor.close()

def consultar_produtos(connection):
    """
    Consulta todos os produtos da tabela 'produtos'.
    """
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()
        print("Produtos na tabela:")
        for produto in produtos:
            print(produto)
    except sqlite3.Error as e:
        print(f"Erro ao consultar produtos: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    conn = conectar()
    if conn:
        criar_tabela(conn)
        inserir_produto(conn, 'Produto A', 10.99)
        inserir_produto(conn, 'Produto B', 20.50)
        consultar_produtos(conn)
        conn.close()