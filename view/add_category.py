import tkinter as tk
from src.functions import show_message

def show_add_category(
  editor, 
  categories, 
  selected_category, 
  display_categories_optionmenu, 
  display_descriptions, 
  add_description):
  
  def confirm_add_category(event=None):
    new_cat = entry_new_cat.get().strip()
    if not new_cat:
      show_message("error", "O nome da categoria não pode ser vazio.")
      return
    if new_cat in categories:
      show_message("error", "Categoria já existe!")
      return
    
    categories[new_cat] = []
    display_categories_optionmenu()
    selected_category.set(new_cat)
    add_description()
    display_descriptions(new_cat)
    add_cat_window.destroy()
  
  def close_add_category(event=None):
    add_cat_window.destroy()

  add_cat_window = tk.Toplevel(editor)
  add_cat_window.title("Adicionar Categoria")
  add_cat_window.grab_set()  # Foco na nova janela
  add_cat_window.bind('<Escape>', close_add_category) # Fecha ao teclar ESC

  tk.Label(add_cat_window, text="Categoria:").pack(padx=10, pady=10)
  entry_new_cat = tk.Entry(add_cat_window, width=30)
  entry_new_cat.pack(padx=10, pady=(0, 10))
  entry_new_cat.focus_set()
  entry_new_cat.bind('<Return>', confirm_add_category) # Confirma ao teclar ENTER

  frame_buttons = tk.Frame(add_cat_window)
  frame_buttons.pack(pady=10)

  btn_confirm = tk.Button(frame_buttons, text="Confirmar", command=confirm_add_category)
  btn_confirm.pack(side='left', padx=5)

  btn_close = tk.Button(frame_buttons, text="Fechar", command=close_add_category)
  btn_close.pack(side='left', padx=5)