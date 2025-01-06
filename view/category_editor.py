import tkinter as tk
from tkinter import messagebox
from src.functions import load_json, save_json, show_message
from .add_category import show_add_category

# Função para abrir o editor de categorias
def open_category_editor(root, category_file_path, entry_categories):
	# Exibe as categorias no optionmenu
	def display_categories_optionmenu():
		menu = option_menu['menu']
		menu.delete(0, 'end')
		for category in categories:
			menu.add_command(label=category, command=lambda c=category: on_category_select(c))
		if categories:
			selected_category.set(next(iter(categories)))  # Seleciona a primeira categoria por padrão
		pass

	def on_category_select(category):
		selected_category.set(category)
		display_descriptions(category)

	# Exibe todas as descrições de uma categoria na tela
	def display_descriptions(category):
    # Limpa o frame de descrições para exibir as novas entradas
		for widget in frame_descriptions.winfo_children():
			widget.destroy()

    # Limpa a lista de entradas de descrições
		entries_descriptions.clear()

    # Carrega as descrições existentes ou uma lista vazia
		descriptions = categories.get(category, [])

		last_entry = None  # Variável para armazenar a última entry

    # Exibe as descrições (no máximo 4 por linha)
		for idx, desc in enumerate(descriptions):
			row = idx // 4
			col = (idx % 4) * 2  # Espaçamento entre as colunas para o botão de remover

			# Cria uma nova entry para cada descrição
			entry = tk.Entry(frame_descriptions, width=20)
			entry.grid(row=row, column=col, padx=(0,0), pady=4, sticky='w')
			entry.insert(0, desc)
			entries_descriptions.append(entry)

			# Função chamada quando o foco sai da entry
			def update_description(event, index=idx):
					categories[category][index] = event.widget.get().strip()

			# Adiciona o evento de foco para atualizar a descrição
			entry.bind("<FocusOut>", update_description)

			last_entry = entry

			# Botão de remover ao lado da entry
			btn_remove_desc = tk.Button(frame_descriptions, text="-", fg="red", command=lambda e=entry: remove_description(e))
			btn_remove_desc.grid(row=row, column=col + 1, padx=(0, 10), pady=10, sticky='w')
		
		if last_entry:
			last_entry.focus_set()
		pass

	# Remove a categoria selecionada da tela 
	def remove_category():
		category = selected_category.get()
		if not category:
			show_message("error", "Nenhuma categoria selecionada.")
			return
		confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover a categoria '{category}'?")
		if confirm:
			del categories[category]
			display_categories_optionmenu()
			if categories:
				selected_category.set(next(iter(categories)))
				display_descriptions(selected_category.get())
			else:
				# Limpa as descrições se não houver categorias
				for widget in frame_descriptions.winfo_children():
					widget.destroy()

	# Adiciona uma nova descrição vazia para a categoria selecionada
	def add_description():
    # Certifica-se de que há uma categoria selecionada
		current_category = selected_category.get()
		if not current_category:
			show_message("error", "Nenhuma categoria selecionada.")
			return

    # Armazena as descrições atuais antes de adicionar uma nova
		current_descriptions = [entry.get().strip() for entry in entries_descriptions]
    
    # Adiciona uma nova descrição vazia
		current_descriptions.append("")

    # Atualiza as descrições da categoria no dicionário global de categorias
		categories[current_category] = current_descriptions

    # Reexibe as descrições, incluindo a nova entrada vazia
		display_descriptions(current_category)

	# Remove a descrição recebida da categoria selecionada
	def remove_description(entry):
		category = selected_category.get()
		if not category:
				show_message("error", "Nenhuma categoria selecionada.")
				return

		# Obtém o índice da descrição na lista de entries
		index = entries_descriptions.index(entry)

		# Obtém o valor da descrição
		desc = entry.get().strip()

		# Se a descrição estiver vazia, apenas remove a entry e a posição correspondente no dicionário
		if not desc:
				categories[category].pop(index)
				entries_descriptions.remove(entry)
				display_descriptions(category)
				return

		# Confirma se o usuário deseja remover a descrição
		confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover a descrição '{desc}'?")
		if confirm:
				# Verifica se o índice existe no dicionário e remove com base no índice
				if index < len(categories[category]):
						categories[category].pop(index)
				entries_descriptions.remove(entry)
				display_descriptions(category)

	# Salva o arquivo de categorias
	def save_all_categories():
		nonlocal category_file_path
		current_category = selected_category.get()

		if not current_category:
			show_message("error", "Nenhuma categoria selecionada.")
			return

		updated_descriptions = []

		for entry in entries_descriptions:
			desc = entry.get().strip()
			if desc:
				updated_descriptions.append(desc)

		if current_category:
			categories[current_category] = updated_descriptions  # Atualiza a categoria selecionada com as descrições

		new_file = save_json(category_file_path, categories)

		if new_file:
			category_file_path = new_file

			entry_categories.delete(0, tk.END)
			entry_categories.insert(0, new_file)

			entry_file.config(state='normal')
			entry_file.delete(0, tk.END)
			entry_file.insert(0, new_file)
			entry_file.config(state='readonly')
	
	# Interface do editor
	editor = tk.Toplevel(root)
	editor.title("Editar Categorias")

	# Container principal
	frame_main = tk.Frame(editor)
	frame_main.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

	# File
	label_file = tk.Label(frame_main, text="Arquivo de Categorias:")
	label_file.pack(anchor='w', pady=(0, 5))

	entry_file = tk.Entry(frame_main, width=70)
	entry_file.pack(fill='x', pady=(0, 5))
	entry_file.insert(0, category_file_path if category_file_path else "Nenhum arquivo selecionado")
	entry_file.config(state='readonly')

	# Frame para seleção de categoria e botões
	frame_category = tk.Frame(frame_main)
	frame_category.pack(fill=tk.X, pady=(5, 5))

	label_category = tk.Label(frame_category, text="Categoria:", anchor='w')
	label_category.pack(anchor='w', pady=(0, 5))

	selected_category = tk.StringVar(value=" ")
	option_menu = tk.OptionMenu(frame_category, selected_category, "")
	option_menu.config(width=15)
	option_menu.pack(side='left', padx=(2, 0))

	btn_add_cat = tk.Button(frame_category, text="+", 
												 command=lambda: show_add_category(
													 editor, 
													 categories, 
													 selected_category, 
													 display_categories_optionmenu, 
													 display_descriptions, 
													 add_description))
	btn_add_cat.pack(side='left', padx=(2, 0), pady=(0,5))

	btn_remove_cat = tk.Button(frame_category, text="-", command=remove_category)
	btn_remove_cat.pack(side='left', padx=(0,2), pady=(0,5))

	btn_add_desc = tk.Button(frame_category, text="Adicionar Descrição", command=add_description)
	btn_add_desc.pack(side='left', padx=(1,0), pady=(0,5))

	# Frame para exibir as descrições
	frame_descriptions = tk.Frame(frame_main)
	frame_descriptions.pack(fill='both', expand=True)

	entries_descriptions = []  # Lista para manter referências das entries de descrições

	# Frame para loading_label, btn_quit e btn_report
	action_frame = tk.Frame(frame_main)
	action_frame.pack(fill=tk.X, pady=20)

	# Botão Fechar
	btn_close = tk.Button(action_frame, text="Fechar", command=editor.destroy)
	btn_close.pack(side='right', padx=(0,5), pady=10)
	
	# Botão para salvar todas as categorias
	btn_save = tk.Button(action_frame, text="Salvar Categorias", command=save_all_categories)
	btn_save.pack(side='right', padx=0, pady=10)

	# Inicializa as categorias
	try:
		categories = load_json(category_file_path) if category_file_path else {}
	except Exception as e:
		show_message("error", f"Falha ao carregar o arquivo JSON: {e}")
		categories = {}

	display_categories_optionmenu()

	if categories:
		# Seleciona a primeira categoria por padrão
		first_category = next(iter(categories))
		selected_category.set(first_category)
		display_descriptions(first_category)

