import streamlit as st
import mysql.connector
import pandas as pd

def altcodprod():
    import streamlit as st
import mysql.connector
import pandas as pd


def carregar_dados_tabela_conversao():
    # Cria a conexão com o banco de dados
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="mateus_ramos",
        password="flamengo4422",
        database="prodcat"
    )

    # Define a consulta SQL
    sql = "SELECT * FROM tabela_conversao"

    # Executa a consulta SQL e obtém os resultados
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()

    # Obtém os nomes das colunas
    columns = [desc[0] for desc in cursor.description]

    # Fecha o cursor
    cursor.close()

    # Cria o DataFrame com os dados e as colunas
    df = pd.DataFrame(data, columns=columns)

    # Fecha a conexão com o banco de dados
    conn.close()

    return df

def exibir_dados_tabela_conversao():
    # Carrega os dados da tabela_conversao
    df = carregar_dados_tabela_conversao()

    # Exibe os dados usando o Streamlit
    st.title("Dados da tabela_conversao")
    st.dataframe(df)

if __name__ == "__main__":


    altcodprod()
