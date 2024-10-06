import tkinter as tk
from tkinter import messagebox
from src.functions import load_json, save_json

# Função para abrir o editor de categorias
def open_category_editor(root, category_file_path, entry_categories):
  def display_categories(data):
    for widget in frame_content.winfo_children():
      widget.destroy()

    for category, descriptions in data.items():
      # Cria um frame para cada categoria
      category_frame = tk.Frame(frame_content)
      category_frame.pack(fill='x', pady=5)

      # Campo para editar o nome da categoria
      entry_category = tk.Entry(category_frame, width=20)
      entry_category.pack(side='left', padx=(0, 10))
      entry_category.insert(0, category)

      # Campo para editar as descrições
      entry_descriptions = tk.Entry(category_frame, width=70)
      entry_descriptions.pack(side='left', padx=(0, 10))
      entry_descriptions.insert(0, ', '.join(descriptions))

      # Botão para remover a categoria com confirmação
      btn_remove = tk.Button(category_frame, text="Remover", fg="red", command=lambda c=category: remove_category(c))
      btn_remove.pack(side='left')

  def remove_category(category):
    confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover a categoria '{category}'?")
    if confirm:
      del categories[category]
      display_categories(categories)

  def add_category():
    category = entry_new_category.get().strip()
    if category and category not in categories:
      categories[category] = []
      display_categories(categories)
      entry_new_category.delete(0, tk.END)
    else:
      messagebox.showerror("Erro", "Categoria já existe ou inválida!")
  
  def save_all_categories():
    updated_categories = {}
    for child in frame_content.winfo_children():
      entry_category = child.winfo_children()[0]
      entry_descriptions = child.winfo_children()[1]
      category_name = entry_category.get().strip()
      descriptions = [desc.strip() for desc in entry_descriptions.get().split(",") if desc.strip()]
      if category_name:
        updated_categories[category_name] = descriptions
      else:
        messagebox.showerror("Erro", "O nome da categoria não pode ser vazio.")
        return

    # Atualiza o dicionário global de categorias
    categories.clear()
    categories.update(updated_categories)

    # Salva no arquivo JSON
    new_file = save_json(category_file_path, categories)
    
    if new_file:
      entry_categories.delete(0, tk.END)
      entry_categories.insert(0, new_file)
    
    editor.destroy()

  # Interface do editor
  editor = tk.Toplevel(root)
  editor.title("Editar Categorias")

  frame_file = tk.Frame(editor)
  frame_file.pack(pady=10, fill='x')

  tk.Label(frame_file, text="Arquivo de Categorias:").pack(side='left')
  entry_file = tk.Entry(frame_file, width=70)
  entry_file.pack(side='left', padx=(5, 10))
  entry_file.insert(0, category_file_path if category_file_path else "Nenhum arquivo selecionado")
  entry_file.config(state='readonly')

  frame_content = tk.Frame(editor)
  frame_content.pack(pady=10, fill='x')

  # Frame para adicionar nova categoria
  frame_new_category = tk.Frame(editor)
  frame_new_category.pack(pady=10, fill='x')

  tk.Label(frame_new_category, text="Nova Categoria:").pack(side='left')
  entry_new_category = tk.Entry(frame_new_category, width=30)
  entry_new_category.pack(side='left', padx=(5, 10))
  btn_add_category = tk.Button(frame_new_category, text="Adicionar", command=add_category)
  btn_add_category.pack(side='left')

  # Botão para salvar todas as categorias
  btn_save = tk.Button(editor, text="Salvar Categorias", command=save_all_categories)
  btn_save.pack(pady=10)

  # Inicializa as categorias
  categories = load_json(category_file_path) if category_file_path else {}
  display_categories(categories)