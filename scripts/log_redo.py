# Pacote do regex
import re

# Scripts para impressão
from scripts.print_out import print_transactions, print_json, print_update

def find_checkpoint(file):
  # Encontrando o checkpoint e salvando as transações que ainda não terminaram
  matches = re.findall('<CKPT \((.+?)\)>', file.read())
  # Retorna transações do último checkpoint, se não tiver retorna array vazio
  return matches[-1].split(',') if matches else []

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
        # Cria um array com os valores informados no arquivo de log
        values = matches.group(1).split(',')

        # Retorna a coluna da tupla com o ID informado no arquivo
        cursor.execute('SELECT ' + values[1] + ' FROM data WHERE id = ' + values[0])
        tuple = cursor.fetchone()[0]

        # Confere se o valor antigo que esta no arquivo é igual ao valor que está no BD
        if(int(values[2]) == tuple):
          cursor.execute('UPDATE data SET ' + values[1] + ' = ' + values[3] + ' WHERE id = ' + values[0])
          print_update(transaction, tuple, values)


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

    # Imprime saída
    print_transactions(checkpoint_transactions, committed_transactions)
    print_json(cursor)

  finally:
    # Fecha arquivo
    file.close()
