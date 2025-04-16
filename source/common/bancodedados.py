import mysql.connector
from mysql.connector import Error

class BancoDeDados:
    def __init__(self, host="localhost", database="nome_do_banco", user="seu_usuario", password="sua_senha"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def conectar(self):
        try:
            # Tentamos conectar ao banco de dados MySQL
            self.conn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.conn.is_connected():
                print("Conectado ao banco de dados com sucesso!")
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def desconectar(self):
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()
            print("Desconectado do banco de dados.")

    def select(self, query, params=None):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            return resultados
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
        finally:
            cursor.close()

    def insert(self, query, params=None):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            self.conn.commit()
            return resultados
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
        finally:
            cursor.close()


    def create(self, query, params=None):
        try:
            cursor = self.conn.cursor() 
            cursor.execute(query, params)
            self.conn.commit()
            return True
        except Error as e:
            print(f'Erro ao criar tabela: {e}')
            return False
        finally:
            cursor.close()



def selectLogExec(banco, nome_processo):
    query = f"""
    SELECT AUTOR_DA_EMENDA, COUNT(*) AS TOTAL_POR_AUTOR
    FROM {nome_processo}_LOG_EXEC
    GROUP BY AUTOR_DA_EMENDA
    ORDER BY TOTAL_POR_AUTOR DESC
    LIMIT 5;
    """
    resultados = banco.select(query)
    return resultados


def createTable(banco, nome_processo, colunas):
    campos = ""
    for i, coluna in enumerate(colunas):
        coluna_formatada = coluna.replace(" ", "_").replace("-", "_")
        campos += f"`{coluna_formatada}` VARCHAR(255) NULL"
        
        # Adiciona vírgula, exceto após a última coluna
        if i < len(colunas) - 1:
            campos += ", "
    
    query = f"""
    CREATE TABLE IF NOT EXISTS {nome_processo}_LOG_EXEC (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        {campos}
    );
    """
    banco.insert(query)


def insertLogExec(banco, nome_processo, colunas, row):
    import pandas as pd
    valores = [row[coluna] if pd.notna(row[coluna]) else "" for coluna in colunas]
    campos = ", ".join([f"`{coluna.replace(' ', '_').replace('-', '_')}`" for coluna in colunas])
    placeholders = ", ".join(["%s"] * len(colunas))

    query = f"""
    INSERT INTO {nome_processo}_LOG_EXEC (
        {campos}
    ) VALUES (
        {placeholders}
    );
    """

    # Executa o insert com o banco de dados
    banco.insert(query, valores)
