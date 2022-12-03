# Biblioteca do regEx 
import re

def find_checkpoint(file):
  # Encontrando o checkpoint e salvando as transações que ainda não terminaram
  matches = re.findall('<CKPT \((.+?)\)>', file.read())
  # Considerando que vai pegar o último checkpoint do arquivo
  return matches[-1].split(',')

def find_committed_transations(file):
  # Retona pra início do arquivo
  file.seek(0)

  # Encontrando quais transações finalizaram depois do checkpoint  
  transactions = []

  for line in reversed( list(file) ):
    # Só vai percorrer até encontrar um checkpoint
    if ("CKPT" in line): break

    matches = re.search('<commit (.+?)>', line)
    if matches:
      transactions.append(matches.group(1))

  return transactions

def restore_changes(file, committed_transactions, cursor):

  for transaction in committed_transactions:
    # Retona pra início do arquivo
    file.seek(0)

    # Encontrando o início da transação
    content = file.read()
    start_transaction = content.index('<start '+ transaction +'>')
    file.seek(start_transaction)      

    for line in list(file):
      if ('<commit '+ transaction +'>' in line): break

      matches = re.search('<'+ transaction +',(.+?)>', line)
      if matches:
        # Criando um array com os valores informados no arquivo de log
        values = matches.group(1).split(',')

        # Retorna as tuplas com o ID informado no arquivo
        cursor.execute('SELECT ' + values[1] + ' FROM data WHERE id = ' + values[0])
        tuple = cursor.fetchone()[0]
        print(tuple, values)

        # Confere se o valor que esta no arquivo é diferente do valor que está no BD
        if(int(values[3]) != tuple):
          print('No banco, a coluna ' + values[1] +' estava ' + str(tuple) + ' e no log atualizou para ' + values[3])
          cursor.execute('UPDATE data SET ' + values[1] + ' = ' + values[3] + ' WHERE id = ' + values[0])

def print_out(checkpoint_transactions, committed_transactions):
  for transaction in checkpoint_transactions:
    if(transaction in committed_transactions):
      print('Transação '+ transaction +' realizou Redo')
    else:
      print('Transação '+ transaction +' não realizou Redo')
  

def log_redo(cursor):
  # Abre arquivo da entradaLog apenas para leitura
  file = open('test_files/entradaLog', 'r')

  try:
    checkpoint_transactions = find_checkpoint(file)

    committed_transactions = find_committed_transations(file)

    restore_changes(file, committed_transactions, cursor)

    print_out(checkpoint_transactions, committed_transactions)

  finally:
    # Fecha arquivo
    file.close()
