from source.common import bancodedados
from source.pages.navegador import Navegador
from source.common.bancodedados import BancoDeDados

import os
import time
import shutil
import datetime
import unicodedata
import pandas as pd
import seaborn as sns
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
        # Obter os dados do banco
        dados = bancodedados.selectLogExec(banco, nome_processo)
        
        # Criar um DataFrame com os dados
        df = pd.DataFrame(dados, columns=['AUTOR_DA_EMENDA', 'TOTAL_POR_AUTOR'])
        print(df)

        # Configuração do gráfico
        plt.figure(figsize=(12, 8))

        # Gráfico de barras horizontais
        sns.barplot(x='TOTAL_POR_AUTOR', y='AUTOR_DA_EMENDA', data=df, palette='Blues_d', ci=None)

        # Título e rótulos
        plt.title('Top 5 Autores de Emenda', fontsize=16, weight='bold')
        plt.xlabel('Total de Emendas', fontsize=12)
        plt.ylabel('Autor', fontsize=12)

        # Estilo para as barras
        for p in plt.gca().patches:
            p.set_edgecolor('black')
            p.set_linewidth(1)

        # Adicionar valores nas barras
        for index, value in enumerate(df['TOTAL_POR_AUTOR']):
            plt.text(value + 0.2, index, str(value), va='center', fontsize=12)

        # Ajuste dos rótulos do eixo X
        plt.xticks(fontsize=10, rotation=45, ha='right')

        # Ajustes do layout
        plt.tight_layout()

        # Salvar o gráfico em um arquivo PNG com alta resolução
        plt.savefig(r'C:\RPA\ProtótipoEmendasParlamentares\source\images\top5_autores.png', dpi=200, bbox_inches='tight')
        
        # Exibir o gráfi
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
    
