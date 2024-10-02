import csv
from datetime import datetime
from ..functions import categorizar_lancamento

def gera_lancamentos_xp(arquivo_csv, categorias):
  lancamentos = []
  with open(arquivo_csv, mode='r', encoding='latin1') as file:
    leitor_csv = csv.reader(file, delimiter=';')
    
    process = False
    for linha in leitor_csv:
      if linha and not process:
        process = True
        continue
      
      if process and linha:
        data = datetime.strptime(linha[0], '%d/%m/%Y')
        data_formatada = data.strftime('%d/%m')
        desc = linha[1] + f" ({linha[4]})" if linha[4] != '-' else linha[1]
        valor_str = linha[3].replace('R$', '').replace(',', '.').strip()

        # Verificar se o valor não está vazio e tentar converter para float
        if valor_str.strip():
          try:
            valor =  float(valor_str)
          except ValueError:
            continue
        else:
          continue

        if "Pagamentos Validos Normais" not in desc:
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