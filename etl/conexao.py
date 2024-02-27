def conectar(database='bronze'):
    jdbc_url = f"jdbc:mysql://localhost:3306/{database}"
    return jdbc_url

def properties(user="financasp", password="Financasp#321", driver="com.mysql.cj.jdbc.Driver"):
    jdbc_properties = {"user":user,"password":password,"driver":driver}
    return jdbc_properties

def database_table(table='cotahist'):
    return table

password = 'Financasp#321'