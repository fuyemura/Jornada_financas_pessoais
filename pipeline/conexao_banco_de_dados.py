from sqlalchemy import create_engine
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

def database_table(table='cotahist'):
    return table
