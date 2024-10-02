import csv
from ..functions import categorizar_lancamento

def gera_lancamentos_bradesco(arquivo_csv, categorias):
  lancamentos = []
  with open(arquivo_csv, mode='r', encoding='latin1') as file:
    leitor_csv = csv.reader(file, delimiter=';')
    next(leitor_csv)

    process = False
    for linha in leitor_csv:
      if linha and linha[0] == 'Data':
        process = True
        continue
      
      if process and linha:
        data = linha[0]
        desc = linha[1]
        valor_str = linha[3].replace(',', '.')

        # Verificar se o valor não está vazio e tentar converter para float
        if valor_str.strip():
          try:
            valor = float(valor_str)
          except ValueError:
            continue
        else:
          continue

        if "PAG BOLETO BANCARIO" not in desc and "SALDO ANTERIOR" not in desc:
          categoria = categorizar_lancamento(desc, categorias)

          lancamentos.append({
            'data': data,
            'desc': desc,
            'valor': valor,
            'cat': categoria
          })
      else: 
        process = False
  return lancamentos