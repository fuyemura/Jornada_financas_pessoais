from sqlalchemy import create_engine
def conexao_mysql(schema):
    """Está função é usada para conectar o Pycharm ao banco de dados mysql, que está hospedado no servidor local:
    :param = conector
    :param = root
    :param = password
    :param = servidor
    :param = database"""
    return create_engine(f'mysql+mysqlconnector://financasp:Financasp#321@localhost/{schema}')

