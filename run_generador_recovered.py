import sys
import os
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# Ajustar el sys.path si es necesario
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generador_recovered import create_excel_table_final, extract_account_number

def main():
    '''Función principal del wrapper'''
    pdf_path = None
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        if not os.path.exists(pdf_path):
            print(f'Error: El archivo no existe: {pdf_path}')
            sys.exit(1)
    elif not TKINTER_AVAILABLE:
        print('Error: Se requiere tkinter para el diálogo gráfico.')
        print('Uso: python run_generador_recovered.py <ruta_del_pdf>')
        sys.exit(1)
    else:
        root = tk.Tk()
        root.withdraw()
        pdf_path = filedialog.askopenfilename(
            title='Selecciona un PDF de Estado de Cuenta', 
            filetypes=[('PDF files', '*.pdf'), ('All files', '*.*')], 
            initialdir=os.path.expanduser('~')
        )
        root.destroy()
        
    if not pdf_path:
        print('No se seleccionó ningún archivo.')
        sys.exit(0)
        
    print(f'\n============================================================')
    print(f'Procesando: {os.path.basename(pdf_path)}')
    print(f'============================================================')
    
    create_excel_table_final(pdf_path)

if __name__ == '__main__':
    main()
