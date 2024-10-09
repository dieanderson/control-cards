import os, json, platform, subprocess, webbrowser, tempfile
from pathlib import Path
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox, Entry
from collections import defaultdict

def load_json(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    return json.load(file)

def save_json(file_path, data):
  create = False
  if not file_path:
    file_path = filedialog.asksaveasfilename(
      defaultextension=".json",
      filetypes=[("JSON files", "*.json")],
      title="Salvar arquivo de categorias"
    )
    create = True
  
  if file_path:
    try:
      with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
      messagebox.showinfo("Sucesso", f"Categorias salvas em: {file_path}")
      return file_path if create == True else None
    except Exception as e:
      messagebox.showerror("Erro", f"Erro ao salvar categorias: {e}")
  else:
    messagebox.showinfo("Atenção", "Salvamento cancelado pelo usuário")

def select_file(file_type, type_name, entry: Entry):
  file_path = filedialog.askopenfilename(filetypes=[(type_name, file_type)])
  if file_path:
    entry.delete(0, 'end')
    entry.insert(0, file_path)

# Monta URL completa para pasta e arquivo
def get_file_path(folder_name, file_name):
  base_dir = Path(__file__).resolve().parent.parent
  file_path = str(base_dir / folder_name / file_name)
  return file_path

# Abre o PDF no visualizador padrão de acordo com o sistema operacional
def open_file(path):
  if platform.system() == "Darwin":  # macOS
    subprocess.call(('open', path))
  elif platform.system() == "Windows":  # Windows
    os.startfile(path)
  elif platform.system() == "Linux":  # Linux
    subprocess.call(('xdg-open', path))
  else:
    webbrowser.open_new(path)

# Categoriza os lançamentos
def categorizar_lancamento(descricao, categorias):
  descricao = descricao.lower()
  for categoria, termos in categorias.items():
    if any(descricao.startswith(term.lower()) for term in termos):
      return categoria
  return 'Outros'

# Agrupa os lançamentos por categoria e totaliza
def agrupar_por_categoria(lancamentos):
  agrupados = defaultdict(lambda: {"total": 0, "lancamentos": []})

  for lancamento in lancamentos:
    categoria = lancamento['cat']
    valor = lancamento['valor']
    agrupados[categoria]["total"] += valor
    agrupados[categoria]["lancamentos"].append({
      "data": lancamento['data'],
      "desc": lancamento['desc'],
      "valor": lancamento['valor']
    })
  resultado = [{"categoria": cat, "total": info['total'], "lancamentos": info['lancamentos']} for cat, info in agrupados.items()]
  return resultado

# Cria resumo por categoria
def resumo_de_categorias(lancamentos):
  totais_por_categoria = {}
  total_geral = 0

  # Soma os valores por categoria e calcula o total geral
  for lancamento in lancamentos:
    categoria = lancamento['cat']
    valor = lancamento['valor']
    total_geral += valor
    if categoria in totais_por_categoria:
      totais_por_categoria[categoria] += valor
    else:
      totais_por_categoria[categoria] = valor

  # Adiciona o percentual correspondente
  totais_com_percentual = {}
  for categoria, total in totais_por_categoria.items():
    percentual = (total / total_geral) * 100
    totais_com_percentual[categoria] = {
      'total': total,
      'percentual': percentual
    }

  return totais_com_percentual

# Gera gráfico Pizza
def gerar_grafico_pizza(resumo):
  categorias = list(resumo.keys())
  totais = [resumo[categoria]['total'] for categoria in categorias]

  plt.figure(figsize=(9, 7))  # Aumenta o tamanho do gráfico
  wedges, texts, autotexts = plt.pie(
    totais,
    autopct='%1.1f%%',
    startangle=90,
    colors=plt.cm.Paired.colors,
    wedgeprops=dict(width=0.4),  # Faz a pizza ser um gráfico de anel
    pctdistance=0.85  # Afasta os percentuais
  )

  # Formatação dos percentuais
  for autotext in autotexts:
    autotext.set_fontsize(12)  # Define tamanho 
    autotext.set_fontweight('bold')  # Coloca em negrito
    #autotext.set_color('white') # Define a cor

  # Adiciona legendas externas ao gráfico
  plt.legend(
    wedges, 
    categorias, 
    title="Categorias", 
    loc="center left", 
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=12
  )

  # Ajusta o título da legenda
  plt.setp(plt.gca().get_legend().get_title(), fontsize=14, fontweight='bold')

  # Ajusta o espaço entre o gráfico e a legenda
  plt.subplots_adjust(left=0.1, right=0.75)  

  temp_dir = tempfile.gettempdir()
  img_path= os.path.join(temp_dir, 'grafico.png')
  plt.axis('equal')  # Mantém o gráfico circular
  plt.tight_layout()
  plt.savefig(img_path, bbox_inches='tight')
  plt.close()
  return img_path
