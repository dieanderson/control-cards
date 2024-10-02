from .pdf import generate_categorized_pdf
from .functions import agrupar_por_categoria, resumo_de_categorias, get_file_path
from .models.bradesco import gera_lancamentos_bradesco
from .models.nubank import gera_lancamentos_nubank
from .models.xp import gera_lancamentos_xp

def process_csv(arquivo_csv, categorias, cod_banco):
  path_file = get_file_path('files', arquivo_csv)
  lancamentos = []
  
  match cod_banco:
    case 237:
      lancamentos = gera_lancamentos_bradesco(path_file, categorias)
    case 260:
      lancamentos = gera_lancamentos_nubank(path_file, categorias)
    case 348:
      lancamentos = gera_lancamentos_xp(path_file, categorias)

  lancamentos_agrupados = agrupar_por_categoria(lancamentos)
  resumo = resumo_de_categorias(lancamentos)

  generate_categorized_pdf(lancamentos_agrupados, resumo, cod_banco)