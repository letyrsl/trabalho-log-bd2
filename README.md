# Trabalho Prático - LOG - BDII
**Alunas: Évellyn Camatti e Letícia da Rosa**

O objetivo desse trabalho de Banco de Dados II é implementar o mecanismo de log Redo/Undo com checkpoint usando o SGBD. 

## Funcionamento
- O código deverá ser capaz de ler o arquivo de log (entradaLog) e o arquivo de Metadado (metadado.json) e validar as informações no banco de dados através do modelo REDO/UNDO. 
- O código receberá como entrada o arquivo de metadados (dados salvos) e os dados da tabela que irá operar no banco de dados.

Exemplo de tabela do banco de dados: 

  ID  |  A  |  B 
 ---- | --- | ---
  1   | 100 | 20 
  1   |  20 | 30 

Arquivo de log no formato **<transação, “id da tupla”,”coluna”, “valor antigo”, “valor novo”>**

## Exemplo
Arquivo de Metadado: 

```
[ 
  {   "att": "A",   "row"=1, “value”=100 },
  {   "att": "A",   "row"=2, “value”=20  },
  {   "att": "B",   "row"=1, “value”=20  },
  {   "att": "B",   "row"=2, “value”=30  }
]
```

Arquivo de Log: 

```
<start T1>
<T1,1, A,20,30>
<start T2>
<commit T1>
<CKPT (T2)>
<T2,2, A,50>
<start T3>
<CKPT>
<start T4>
<T4,1, A,100>
<commit T4>
```

Saída: 

```
“Transação T2 não realizou Redo”
“Transação T3 não realizou Redo”
“Transação T4 realizou Redo”

[ 
  {   "att": "A",   "row"=1   , “value”=100 },
  {   "att": "A",   "row"=2   , “value”=20  },
  {   "att": "B",   "row"=1   , “value”=20  },
  {   "att": "B",   "row"=2   , “value”=30  }
]
```

O checkpoint Redo permite que parte do log já processada seja descartada para evitar o reprocessamento. 

## Detalhes
Funções a serem implementadas:
- Carregar o banco de dados com a tabela antes de executar o código do log (para zerar as configurações e dados parciais);
- Carregar o arquivo de log;
- Verifique quais transações devem realizar REDO/UNDO. Imprimir o nome das transações que irão sofrer Redo. Observem a questão do checkpoint;
- Checar quais valores estão salvos nas tabelas (com o select) e atualizar valores inconsistentes (update);
- Reportar quais dados foram atualizados;
- Seguir o fluxo de execução conforme o método de REDO, conforme visto em aula; 
