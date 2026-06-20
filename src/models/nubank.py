import csv
from datetime import datetime
from ..functions import categorizar_lancamento

def gera_lancamentos_nubank(arquivo_csv, categorias):
  lancamentos = []
  with open(arquivo_csv, mode='r', encoding='latin1') as file:
    leitor_csv = csv.reader(file, delimiter=',')

    process = False
    for linha in leitor_csv:
      if linha and linha[0] == 'date':
        process = True
        continue
      
      if process and linha:
        data = datetime.strptime(linha[0], '%Y-%m-%d')
        data_formatada = data.strftime('%d/%m')
        desc = linha[1]
        valor_str = linha[2]

        # Verificar se o valor não está vazio e tentar converter para float
        # O Nubank passou a usar formato brasileiro: ponto de milhar e
        # vírgula decimal (ex: "1.501,00"). Normaliza antes de converter.
        if valor_str.strip():
          valor_normalizado = valor_str.strip()
          if ',' in valor_normalizado:
            valor_normalizado = valor_normalizado.replace('.', '').replace(',', '.')
          try:
            valor = float(valor_normalizado)
          except ValueError:
            continue
        else:
          continue

        if "Pagamento recebido" not in desc:
          categoria = categorizar_lancamento(desc, categorias)

          lancamentos.append({
            'data': data_formatada,
            'desc': desc,
            'valor': valor,
            'cat': categoria
          })
      else: 
        process = False
  return lancamentos