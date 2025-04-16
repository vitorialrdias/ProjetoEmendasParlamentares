from source.common import bancodedados
from source.pages.navegador import Navegador
from source.common.bancodedados import BancoDeDados

import os
import time
import shutil
import datetime
import unicodedata
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt


def tratarDownload() -> str:
    # Nessa função fazemos o tratamento do nome do arquivo, movendo o mesmo para a pasta destinada
    try:    
        caminho_pasta = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        nome_arquivo = "emendas"
        arquivo = (fr'{caminho_pasta}\{nome_arquivo}.csv')

        print(arquivo)

        if not arquivo:
            print('Arquivo não encontrado!')
            return
        
        
        caminho_destino = os.path.join(os.environ['USERPROFILE'], 'Documentos', 'Emendas Educacao')
        if not os.path.exists(caminho_destino):
            os.makedirs(caminho_destino)


        date = datetime.datetime.now().year

        novo_nome_arquivo = f"Emendas Parlamentares Escolas {date}.csv"
        novo_caminho_arquivo = os.path.join(caminho_destino, novo_nome_arquivo)
        novo_caminho_arquivo = os.path.normpath(novo_caminho_arquivo) 

        shutil.move(arquivo, novo_caminho_arquivo)
        print(f"Arquivo foi movido e renomeado para {novo_caminho_arquivo} com sucesso!")

        return novo_caminho_arquivo
    except Exception as e:
        print(f'Erro ao tratar nome do arquivo: {e}')
        return None
    
def lerArquivoCSV(banco, nome_processo, caminho_arquivo) -> bool:
    # Nessa função realizamos a leitura do arquivo e inserção no banco de dados
    try:
        df = pd.read_csv(caminho_arquivo, sep=';')
        
        # Normalizamos os dados retirando os acentos e colocamos em uppercaze
        df.columns = [unicodedata.normalize('NFKD', coluna).encode('ASCII', 'ignore').decode('utf-8').upper() for coluna in df.columns]       
        for coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda x: unicodedata.normalize('NFKD', str(x)).encode('ASCII', 'ignore').decode('utf-8').upper() if pd.notna(x) else x)

        colunas = df.columns.tolist()



        # Criamos a tabela dinamicamente
        bancodedados.createTable(banco, nome_processo, colunas)
        
        # Inserimos os dados após a criação da tabela
        for index, row in df.iterrows():
            bancodedados.insertLogExec(banco, nome_processo, colunas, row)

            
        print(f'Tabela criada com sucesso: {nome_processo}_LOG_EXEC')
        return True

    except Exception as e:
        print(f'Erro ao tentar ler arquivo: {e}')
        return False

def uploadDados(banco, nome_processo) -> bool:
    # Nessa função carregamos os dados para retornar em um gráfico 
    try:
        dados = bancodedados.selectLogExec(banco, nome_processo)

        df = pd.DataFrame(dados, columns=['AUTOR_DA_EMENDA', 'TOTAL_POR_AUTOR'])
        print(df)

        plt.figure(figsize=(10, 6))
        plt.bar(df['AUTOR_DA_EMENDA'], df['TOTAL_POR_AUTOR'], color='skyblue')

        plt.title('Top 5 Autores de Emenda')
        plt.xlabel('Autor')
        plt.ylabel('Total de Emendas')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(r'C:\RPA\ProtótipoEmendasParlamentares\source\images\top5_autores.png', dpi=200, bbox_inches='tight')

        return True
    except Exception as e:
        print(f'Erro ao tentar criar gráfico demonstrativo. {e}')
        return False


def main():
    # Função principal de execução do projeto
    try:
        nome_processo = "EXTEMENDA_PARLAMENTAR_EDU"
        url_site = "https://portaldatransparencia.gov.br/"
        load_dotenv(dotenv_path=r'C:\RPA\ProtótipoEmendasParlamentares\database.env')

        # Conexão com o Banco de dados!
        banco = BancoDeDados(host=os.getenv("DB_HOST"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        banco.conectar()

        success = False
        while not success:  # Enquanto o download do arquivo não for bem sucedido, o processo permanece no while.
            site = Navegador(url_site)
            driver = site.openPage()
            site.navSite(driver)
            site.filtroPesquisa(driver)
            success = site.downloadArquivo(driver)
        caminho_arquivo = tratarDownload()
        if caminho_arquivo != None:
            lerArquivoCSV(banco, nome_processo, caminho_arquivo)
            grafico = uploadDados(banco, nome_processo)
            if grafico:
                print(f'''
                Grafico criado com sucesso, acesse na pasta: 
                 
                AnaliseEmendasParlamentares\source\images''')

    except Exception as e:
        print(f"Erro ao executar o processo: {e}")
    
    # Aqui desconectamos do Banco de dados!
    banco.desconectar()

if __name__ == '__main__':
    main()
    
