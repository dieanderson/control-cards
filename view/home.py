import tkinter as tk
from src.process import run_process
from src.functions import select_file
from data.banks import banks
from view.category_editor import open_category_editor

def start_app():
  # Criação da interface
  root = tk.Tk()
  root.title("Control Cards")

  # Labels e entradas para o nome do arquivo e código do banco
  tk.Label(root, text="Extrato (CSV):", anchor='w').grid(row=0, column=0, padx=10, pady=10, sticky='w')
  entry_csv = tk.Entry(root, width=50)
  entry_csv.grid(row=0, column=1, padx=0, pady=10)

  btn_sel_file_csv = tk.Button(root, text="Selecionar", command=lambda: select_file("*.csv", "CSV Files", entry_csv))
  btn_sel_file_csv.grid(row=0, column=2, padx=5, pady=10)

  tk.Label(root, text="Categorias:", anchor='w').grid(row=1, column=0, padx=10, pady=10, sticky='w')
  entry_categories = tk.Entry(root, width=50)
  entry_categories.grid(row=1, column=1, padx=0, pady=10)

  btn_sel_file_json = tk.Button(root, text="Selecionar", command=lambda: select_file("*.json", "JSON Files" , entry_categories))
  btn_sel_file_json.grid(row=1, column=2, padx=5, pady=10)

  btn_edit_categories = tk.Button(root, text="Editar Categorias", command=lambda: open_category_editor(root, entry_categories.get(), entry_categories))
  btn_edit_categories.grid(row=1, column=3, padx=(0, 10), pady=10)

  bank = tk.StringVar()
  bank.set(list(banks.values())[0])

  tk.Label(root, text="Banco:", anchor='w').grid(row=2, column=0, padx=10, pady=10, sticky='w')
  bank_selector = tk.OptionMenu(root, bank, *banks.values())
  bank_selector.config(width=15)
  bank_selector.grid(row=2, column=1, padx=0, pady=10, sticky='w')

  # Botão gerar relatório
  btn_report = tk.Button(root, text="Gerar Relatório", command=lambda: run_process(entry_csv.get(), bank.get(), entry_categories.get()))
  btn_report.grid(row=3, column=0, padx=10, pady=30, sticky='ew')

  # Botão sair
  btn_report = tk.Button(root, text="Sair", command=root.quit)
  btn_report.grid(row=3, column=1, padx=0, pady=30, sticky='w')

  # Executa a interface
  root.mainloop()