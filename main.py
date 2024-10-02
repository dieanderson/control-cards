from src.process import process_csv
from data.categorias import categorias

def main():
    # Cód Bancos: Bradesco(237), Nubank(260), XP(348)
    process_csv('nubank-2024-09.csv', categorias, 260)
    
if __name__ == "__main__":
    main()