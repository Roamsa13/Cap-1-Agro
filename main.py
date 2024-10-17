import inserir_dados

def main():
    """
    Executa a inserção de dados e, em seguida, consulta e exibe os dados.
    """
    print("Iniciando inserção de dados...\n")
    
    conn = inserir_dados.conectar()  # Conecta ao banco de dados
    if conn:
        inserir_dados.criar_tabela(conn)
        inserir_dados.inserir_produto(conn, 'Produto A', 10.99)
        inserir_dados.inserir_produto(conn, 'Produto B', 20.50)
        print("\nInserção de dados concluída.")
        
        print("\nConsultando e exibindo dados...\n")
        inserir_dados.consultar_produtos(conn)
        
        conn.close()  # Fechando a conexão

if __name__ == "__main__":
    main()