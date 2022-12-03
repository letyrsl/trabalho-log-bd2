# Biblioteca do regEx 
import re

def find_checkpoint(file):
  # Encontrando o checkpoint e salvando as transações que ainda não terminaram
  transactions = []

  for line in reversed( list(file) ):
    matches = re.search('<CKPT \((.+?)\)>', line)
    if matches:
      transactions.append(matches.group(1).split(","))
      break

  # Retona pra início do arquivo
  file.seek(0)

  return transactions

def find_committed_transations(file):
  # Encontrando quais transações finalizaram depois do checkpoint  
  transactions = []

  for line in reversed( list(file) ):
    # Só vai percorrer até encontrar um checkpoint
    if ("CKPT" in line): break

    matches = re.search('<commit (.+?)>', line)
    if matches:
      transactions.append(matches.group(1))

  # Retona pra início do arquivo
  file.seek(0)

  return transactions

def log_redo(cursor):
  # Abre arquivo da entradaLog apenas para leitura
  file = open('test_files/entradaLog', 'r')

  try:
    checkpoint_transactions = find_checkpoint(file)

    committed_transactions = find_committed_transations(file)

    print(checkpoint_transactions, committed_transactions)

  finally:
    # Fecha arquivo
    file.close()
