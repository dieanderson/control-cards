import locale
from fpdf import FPDF
from .functions import get_file_path, gerar_grafico_pizza

# Gera PDF
def generate_categorized_pdf(lancamentos_agrupados, resumo, cod_banco):
  locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
  banco_nome = ''
  banco_img = ''
  nome_arquivo= get_file_path('reports', 'relatorio.pdf')
  match cod_banco:
    case 237:
      banco_nome = 'Bradesco'
      banco_img = get_file_path('img', 'bradesco.png')
      nome_arquivo = get_file_path('reports', 'relatorio_bradesco.pdf')
    case 260:
      banco_nome = 'Nubank'
      banco_img = get_file_path('img', 'nubank.png')
      nome_arquivo = get_file_path('reports', 'relatorio_nubank.pdf')
    case 348:
      banco_nome = 'XP'
      banco_img = get_file_path('img', 'xp.png')
      nome_arquivo = get_file_path('reports', 'relatorio_xp.pdf')

  pdf = FPDF()
  pdf.set_auto_page_break(auto=True, margin=15)
  pdf.add_page()
  
  # Logo Banco
  pdf.image(banco_img, x=10, y=0, w=25)

  # Título
  pdf.set_font('Arial', 'B', 12)
  pdf.cell(200, 10, f'Cartão {banco_nome}: Lançamentos Categorizados', ln=True, align='C')

  # Lançamentos *************************************************
  pdf.set_font('Arial', 'B', 10)
  pdf.cell(200, 10, 'Lançamentos', ln=True, align='C')
  for categoria in lancamentos_agrupados:
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(0, 6, 'Categoria:', border=0)
    pdf.set_font('Arial', '', 8)
    pdf.set_x(25)
    pdf.cell(0, 6, categoria['categoria'], ln=True)
    
    # Cabeçalho Lançamentos
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(25, 4, 'Data', border=0)
    pdf.cell(100, 4, 'Descrição', border=0)
    pdf.cell(25, 4, 'Valor', border=0, align='R', ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Linha separadora

    # Lançamentos
    pdf.set_font('Arial', '', 8)
    for lancamento in categoria['lancamentos']:
      pdf.cell(25, 4, lancamento['data'], border=0)
      pdf.cell(100, 4, lancamento['desc'], border=0)
      pdf.cell(25, 4, locale.currency(lancamento['valor'], grouping=True, symbol=False), border=0, align='R', ln=True)

    # Total
    pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Linha separadora
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(0, 8, f"Total: R$ {locale.currency(categoria['total'], grouping=True, symbol=False)}", ln=True)

    pdf.ln(8)
  # Lançamentos *************************************************

  y_pos_grafico_start = pdf.get_y() # Captura posição inicial para o gráfico

  # Resumo ******************************************************
  pdf.set_font('Arial', 'B', 10)
  pdf.cell(200, 10, 'Resumo:', ln=True)
  
  # Cabeçalho Resumo
  pdf.cell(30, 5, 'Categoria', border=0)
  pdf.cell(30, 5, 'Total', border=0, align='R')
  pdf.cell(20, 5, 'Percent.', border=0, align='R', ln=True)
  pdf.line(10, pdf.get_y(), 100, pdf.get_y()) # Linha separadora
  # Categorias Resumo
  sumTotal = 0
  sumPerc = 0
  pdf.set_font('Arial', '', 8)
  for categoria, dados in resumo.items():
    sumTotal += float(dados['total'])
    sumPerc += float(dados['percentual'])
    pdf.cell(30, 5, categoria, border=0)
    pdf.cell(30, 5, locale.currency(dados['total'], grouping=True, symbol=False), border=0, align='R')
    pdf.cell(20, 5, f"{float(dados['percentual']):.2f} %", border=0, align='R', ln=True)
  pdf.line(10, pdf.get_y(), 100, pdf.get_y()) # Linha separadora
  pdf.set_font('Arial', 'B', 8)
  pdf.cell(30, 5, 'Total:', border=0)
  pdf.cell(30, 5, locale.currency(sumTotal, grouping=True, symbol=False), border=0, align='R')
  pdf.cell(20, 5, f"{sumPerc:.2f} %", border=0, align='R', ln=True)
  pdf.ln(8)
  # Resumo ******************************************************

  # Grafico *****************************************************
  gerar_grafico_pizza(resumo)
  pdf.image(get_file_path('img', 'grafico.png'), x=120, y=y_pos_grafico_start, w=85)
  # Grafico *****************************************************
  
  pdf.output(nome_arquivo)
  print(f'Relatório gerado: {nome_arquivo}')
  return nome_arquivo