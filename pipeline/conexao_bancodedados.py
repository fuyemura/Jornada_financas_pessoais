from sqlalchemy import create_engine, text

def conexao_mysql(schema):
    """Está função é usada para conectar o Pycharm ao banco de dados mysql, que está hospedado no servidor local:
    :param = conector
    :param = root
    :param = password
    :param = servidor
    :param = database"""
    return create_engine(f'mysql+mysqlconnector://financasp:Financasp#321@localhost/{schema}')

def connection(database='bronze'):
    jdbc_url = f"jdbc:mysql://localhost:3306/{database}"
    return jdbc_url

def properties(user="financasp", password="Financasp#321", driver="com.mysql.cj.jdbc.Driver"):
    jdbc_properties = {"user":user,"password":password,"driver":driver}
    return jdbc_properties

def truncate_table(database='bronze', tablename='cotahist'):
    engine = conexao_mysql(database)
    with engine.connect() as conexao:
        conexao.execute(text(f"TRUNCATE TABLE {database}.{tablename}"))
