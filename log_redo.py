# Biblioteca do regEx 
import re

def log_redo(cursor):
  # Abre arquivo da entradaLog apenas para leitura
  file = open('test_files/entradaLog', 'r')

  try:
    # Encontrando o checkpoint e salvando as transações que ainda não terminaram
    checkpoint_transactions = []
    for line in reversed( list(file) ):
      matches = re.search('<CKPT \((.+?)\)>', line)
      if matches:
        transactions = matches.group(1)
        checkpoint_transactions.append(transactions.split(","))
        break
    
    # Retonar pra início do arquivo
    file.seek(0)

    # Encontrando quais transações finalizaram depois do checkpoint  
    committed_transactions = []
    for line in reversed( list(file) ):
      matches = re.search('<commit (.+?)>', line)
      if matches:
        transactions = matches.group(1)
        committed_transactions.append(transactions.split(","))

    print(committed_transactions)
      
  finally:
    # Fecha arquivo
    file.close()
