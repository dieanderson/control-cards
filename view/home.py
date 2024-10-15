import tkinter as tk
from src.process import run_process
from src.functions import select_file
from data.banks import banks
from view.category_editor import open_category_editor

def hide_loading():
    loading_label.config(text="") 
    btn_report.config(state='normal')

def show_loading():
    loading_label.config(text="Gerando relatório, por favor, aguarde...") 
    btn_report.config(state='disabled')

def generate_report(entry_csv, bank, entry_categories):
    # Impede tentativa de execução quando botão desabilitado
    if btn_report['state'] == 'disabled':
        return
    # Valida se CSV e Categorias informados
    if not entry_csv or not entry_categories:
        loading_label.config(text="Por favor, informar o Extrato CSV e o arquivo de Categorias")
        root.after(3000, hide_loading)
        return
   
    show_loading()
    root.update()
    run_process(entry_csv, bank, entry_categories)
    loading_label.config(text="Relatório gerado com sucesso!")
    root.after(3000, hide_loading)

def start_app():
    global root, btn_report, loading_label
    root = tk.Tk()
    root.title("Control Cards")

    # Container principal
    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Extrato (CSV)
    label_csv = tk.Label(main_frame, text="Extrato (CSV):", anchor='w')
    label_csv.pack(anchor='w', pady=(0, 5))
    
    # Frame para entry_csv e btn_sel_file_csv
    csv_frame = tk.Frame(main_frame)
    csv_frame.pack(fill=tk.X, pady=(0, 10))

    entry_csv = tk.Entry(csv_frame, width=50)
    entry_csv.pack(side=tk.LEFT, fill=tk.X, expand=True)

    btn_sel_file_csv = tk.Button(csv_frame, text="Selecionar", command=lambda: select_file("*.csv", "CSV Files", entry_csv))
    btn_sel_file_csv.pack(side=tk.LEFT, padx=5)

    # Categorias
    label_categories = tk.Label(main_frame, text="Categorias:", anchor='w')
    label_categories.pack(anchor='w', pady=(0, 5))

    # Frame para entry_categories, btn_sel_file_json e btn_edit_categories
    category_frame = tk.Frame(main_frame)
    category_frame.pack(fill=tk.X, pady=(0, 10))

    entry_categories = tk.Entry(category_frame, width=50)
    entry_categories.pack(side=tk.LEFT, fill=tk.X, expand=True)

    btn_sel_file_json = tk.Button(category_frame, text="Selecionar", command=lambda: select_file("*.json", "JSON Files", entry_categories))
    btn_sel_file_json.pack(side=tk.LEFT, padx=5)

    btn_edit_categories = tk.Button(category_frame, text="Editar Categorias", command=lambda: open_category_editor(root, entry_categories.get(), entry_categories))
    btn_edit_categories.pack(side=tk.LEFT, padx=5)

    # Banco
    bank = tk.StringVar()
    bank.set(list(banks.values())[0])

    label_bank = tk.Label(main_frame, text="Banco:", anchor='w')
    label_bank.pack(anchor='w', pady=(10, 5))

    bank_selector = tk.OptionMenu(main_frame, bank, *banks.values())
    bank_selector.config(width=15)
    bank_selector.pack(anchor='w')

    # Frame para loading_label, btn_quit e btn_report
    action_frame = tk.Frame(main_frame)
    action_frame.pack(fill=tk.X, pady=20)

    # Label para exibir status
    loading_label = tk.Label(action_frame, text="", fg="red")
    loading_label.pack(side=tk.LEFT)

    # Botão Sair
    btn_quit = tk.Button(action_frame, text="Sair", command=root.quit)
    btn_quit.pack(side=tk.RIGHT, padx=5)

    # Botão Gerar Relatório
    btn_report = tk.Button(action_frame, text="Gerar Relatório", command=lambda: generate_report(entry_csv.get(), bank.get(), entry_categories.get()))
    btn_report.pack(side=tk.RIGHT, padx=5)

    root.mainloop()