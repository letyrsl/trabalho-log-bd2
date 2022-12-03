import json

def create_table():
  cursor.execute('DROP TABLE IF EXISTS data;')

  cursor.execute('''
    CREATE TABLE data (
      id integer NOT NULL,
      a integer NOT NULL,
      b integer NOT NULL
    );
  ''')

def load_database(cursor):
  # Cria tabela data
  create_table

  # Abre arquivo de metadados apenas para leitura
  file = open('test_files/metadado.json', 'r')

  try:
    # Pega dados do arquivo
    data = json.load(file)['INITIAL']
    tuples = list( zip(data['id'], data['A'], data['B']) )

    # Insere tuplas na tabela
    for tuple in tuples:
      values = '('+ str(tuple[0]) +', '+ str(tuple[1]) +', '+ str(tuple[2]) +')'
      insert_query = 'INSERT INTO data(id, a, b) VALUES ' + values
      cursor.execute(insert_query)

  finally:
    # Fecha arquivo
    file.close()
