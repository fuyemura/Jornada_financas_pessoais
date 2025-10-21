import traceback

def connection_mysql(database='bronze'):
    """
    Função para obter a url de conexão do jdbc para o MySQL.
    """
    jdbc_url = f"jdbc:mysql://localhost:3306/{database}"
    return jdbc_url

def properties_mysql(user="financasp", password="Financasp#321", driver="com.mysql.cj.jdbc.Driver"):
    """
    Função para obter usuário, senha e driver do jdbc para o MySQL.
    """
    jdbc_properties = {"user":user,"password":password,"driver":driver}
    return jdbc_properties

def write_pyspark_mysql(df, table_name, database='bronze', mode='append'):
    """
    Função que grava um DataFrame PySpark no MySQL.
    """
    jdbc_url = connection_mysql(database)
    properties = properties_mysql()

    try:
        df.write.jdbc(url=jdbc_url, table=table_name, mode=mode, properties=properties)
        print(f"[SUCESSO] DataFrame gravado na tabela '{table_name}' (mode={mode})!")

    except Exception as e:
        print(f"[ERRO ao gravar PySpark] {e}")
        traceback.print_exc()