import psycopg2
from config import config

def connect():
  conn = None
  try:
    # pega configurações do banco
    params = config()

    # conecta com o banco
    print('Conectando com o PostgreSQL...')
    conn = psycopg2.connect(**params)

    # cria um cursor
    cur = conn.cursor()

	  # teste de execução de select
    print('Versão do PostgreSQL:')
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(db_version)

	  # fecha conexão
    cur.close()

  except (Exception, psycopg2.DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()
      print('Conexão com banco fechada.')


if __name__ == '__main__':
  connect()