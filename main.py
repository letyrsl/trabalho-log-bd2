import psycopg2

from db_config import db_config
from load_database import load_database
from log_redo import log_redo

def main():
  conn = None
  try:
    # conecta com banco de dados e cria cursor
    params = db_config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()

	  # carrega o banco com dados do arquivo
    load_database(cursor)

    # recuperar log REDO
    log_redo(cursor)

    # teste
    cursor.execute('SELECT * FROM data')
    data = cursor.fetchall()
    print(data)

	  # fecha conexão com banco
    cursor.close()

  except (Exception, psycopg2.DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()


if __name__ == '__main__':
  main()
