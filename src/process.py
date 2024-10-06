import os
from tkinter import messagebox
from data.banks import banks
from .pdf import generate_categorized_pdf
from .functions import agrupar_por_categoria, resumo_de_categorias, open_file, load_json
from .models.bradesco import gera_lancamentos_bradesco
from .models.nubank import gera_lancamentos_nubank
from .models.xp import gera_lancamentos_xp

def process_csv(arquivo_csv, categorias, cod_banco):
  lancamentos = []
  
  match cod_banco:
    case 237:
      lancamentos = gera_lancamentos_bradesco(arquivo_csv, categorias)
    case 260:
      lancamentos = gera_lancamentos_nubank(arquivo_csv, categorias)
    case 348:
      lancamentos = gera_lancamentos_xp(arquivo_csv, categorias)

  lancamentos_agrupados = agrupar_por_categoria(lancamentos)
  resumo = resumo_de_categorias(lancamentos)

  pdf_path = generate_categorized_pdf(lancamentos_agrupados, resumo, cod_banco)

  return pdf_path

def run_process(csv, bank, categories_path):
  csv_path = csv
  bank_name = bank
  bank_code = next(code for code, name in banks.items() if name == bank_name)
  categories = load_json(categories_path)
  
  try:
    pdf_path = process_csv(csv_path, categories, int(bank_code))

    if os.path.exists(pdf_path):
      open_file(pdf_path)
    else:
      print(f"O arquivo {pdf_path} não foi encontrado.")

  except Exception as e:
    messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")