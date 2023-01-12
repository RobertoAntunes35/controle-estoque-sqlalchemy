SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha= 'mondistribuidora',
        servidor = 'localhost',
        database = 'controle_estoque',
        )