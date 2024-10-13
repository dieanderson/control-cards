import os
from data.banks import banks
from .pdf import generate_categorized_pdf
from .functions import agrupar_por_categoria, resumo_de_categorias, open_file, load_json, show_message
from .models.bradesco import gera_lancamentos_bradesco
from .models.nubank import gera_lancamentos_nubank
from .models.xp import gera_lancamentos_xp

def run_process(csv_path, bank_name, categories_path):
  bank_code = next(code for code, name in banks.items() if name == bank_name)
  categories = load_json(categories_path)
  
  try:
    lancamentos = []
    ## Gera os lançamentos de acordo com o banco selecionado
    match bank_code:
      case 237:
        lancamentos = gera_lancamentos_bradesco(csv_path, categories)
      case 260:
        lancamentos = gera_lancamentos_nubank(csv_path, categories)
      case 348:
        lancamentos = gera_lancamentos_xp(csv_path, categories)
    
    lancamentos_agrupados = agrupar_por_categoria(lancamentos)
    resumo = resumo_de_categorias(lancamentos)

    pdf_path = generate_categorized_pdf(lancamentos_agrupados, resumo, bank_name)

    if os.path.exists(pdf_path):
      open_file(pdf_path)
    else:
      print(f"O arquivo {pdf_path} não foi encontrado.")

  except Exception as e:
    show_message("error", f"Ocorreu um erro: {str(e)}")