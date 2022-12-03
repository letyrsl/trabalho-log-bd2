def log_redo(cursor):
  # Abre arquivo da entradaLog apenas para leitura
  file = open('test_files/entradaLog', 'r')

  try:
    for line in reversed( list(file) ):
      print(line.rstrip())

  finally:
    # Fecha arquivo
    file.close()
