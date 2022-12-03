# Biblioteca do regEx 
import re

from print_out import print_transactions, print_json

def find_checkpoint(file):
  # Encontrando o checkpoint e salvando as transações que ainda não terminaram
  matches = re.findall('<CKPT \((.+?)\)>', file.read())
  # Considerando que vai pegar o último checkpoint do arquivo
  return matches[-1].split(',')

def find_committed_transations(file):
  transactions = []

  # Retona pra início do arquivo
  file.seek(0)

  # Percorre arquivo de baixo pra cima
  for line in reversed( list(file) ):
    # Só vai percorrer até encontrar um checkpoint
    if ("CKPT" in line): break

    matches = re.search('<commit (.+?)>', line)
    # Se encontra commit, adiciona transição na lista
    if matches:
      transactions.append(matches.group(1))

  # Retorna transações em ordem de commit
  return transactions[::-1]

def restore_changes(file, cursor, committed_transactions):
  # Percorre transações commitadas
  for transaction in committed_transactions:
    # Retorna pra início do arquivo
    file.seek(0)

    # Vai para o início da transação
    content = file.read()
    start_transaction = content.index('<start '+ transaction +'>')
    file.seek(start_transaction)      

    # Percorre arquivo do start da transição até o final
    for line in list(file):
      # Quando chegar no commit da transição, para
      if ('<commit '+ transaction +'>' in line): break

      matches = re.search('<'+ transaction +',(.+?)>', line)
      # Se for log da transação, atualiza no banco
      if matches:
        # Criando um array com os valores informados no arquivo de log
        values = matches.group(1).split(',')

        # Retorna a tupla com o ID informado no arquivo
        cursor.execute('SELECT ' + values[1] + ' FROM data WHERE id = ' + values[0])
        tuple = cursor.fetchone()[0]

        # Confere se o valor que esta no arquivo é diferente do valor que está no BD
        if(int(values[3]) != tuple):
          print('TRANSAÇÃO '+ transaction +': No registro '+ values[0] +', a coluna ' + values[1] +' estava ' + str(tuple) + ' e no log atualizou para ' + values[3])
          cursor.execute('UPDATE data SET ' + values[1] + ' = ' + values[3] + ' WHERE id = ' + values[0])


def log_redo(cursor):
  # Abre arquivo da entradaLog apenas para leitura
  file = open('test_files/entradaLog', 'r')

  try:
    # Pega transações presentes no último checkpoint
    checkpoint_transactions = find_checkpoint(file)

    # Pega transições que foram committadas após o checkpoint
    committed_transactions = find_committed_transations(file)

    # Restaurar mudanças feitas nas transições committadas
    restore_changes(file, cursor, committed_transactions)

    # Imprime 
    print_transactions(checkpoint_transactions, committed_transactions)
    print_json(cursor)

  finally:
    # Fecha arquivo
    file.close()
