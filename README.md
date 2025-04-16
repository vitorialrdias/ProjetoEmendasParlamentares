## Bibliotecas a serem instaladas

### Para tratar dados:
- pandas

### Para visualização de gráficos:
- matplotlib
- seaborn

### Para conexão com banco de dados MySQL:
- mysql-connector-python

### Para automação web:
- selenium
- webdriver-manager

### Para manipulação de datas avançada:
- python-dateutil


## Sobre o Projeto

O projeto tem como objetivo a **extração, tratamento e análise de dados sobre emendas parlamentares voltadas para a área da Educação**.

É realizado uma automação web que acessa o site de emendas parlamentares [Portal Transparencia](https://portaldatransparencia.gov.br/) e segue os passos abaixo:

1. **Aplicação de Filtros:**  
   - Ano: 2024 a 2025  
   - Função: Educação  

2. **Download dos Dados:**  
   Após aplicar os filtros, o sistema realiza o download do arquivo `.csv` contendo as informações filtradas.

3. **Tratamento e Inserção em Banco de Dados:**  
   O arquivo baixado é lido e os dados são tratados e armazenados em uma tabela MySQL.  
   A tabela é criada de forma **dinâmica** durante a execução do código, garantindo flexibilidade para futuras alterações no esquema de dados.

4. **Análise dos Dados:**  
   Com os dados carregados, o sistema realiza uma consulta para identificar os **Top 5 autores de emendas parlamentares destinadas à Educação**.

5. **Geração de Gráfico:**  
   O resultado da análise é representado graficamente e salvo como um arquivo **PNG** no diretório do projeto, dentro da pasta `/images`.

---

> **Nota:**

Emendas parlamentares destinadas à educação costumam ser algo positivo, já que representam investimentos em escolas, universidades e projetos educacionais.  
Mas, como todo recurso público, o impacto real depende de como esses valores são aplicados e fiscalizados. 

---

**Este projeto foi desenvolvido exclusivamente para fins de estudo e portfólio.**  
Os dados são públicos, podendo ser acessado por qualquer pessoa no [Portal Transparencia](https://portaldatransparencia.gov.br/).
O projeto foi desenvolvido utilizando Python como a estrutura principal para automação, tratamento/análise de dados e integração com banco de dados, com o intuito de demonstrar minha experiência nessas áreas.






