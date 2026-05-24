import os
import glob
import re
from generador_recovered import extract_transactions_from_pdf

pdf_dir = r"C:\Users\rizzo\Desktop\bancofer"
pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))

reglas_categorias = {
    'IMPUESTO DEB/CRED': ['gravamenley25413sdeb', 'gravamenley25413scred'],
    'IVA DEBITO': ['ivabase'],
    'COMISIONES Y GASTOS': ['comispservrecaudacion', 'comispserv', 'comis', 'serv', 'comistransfne24'],
    'DEB.TRAN.INTERB-LINK TIT': ['debtraninterblinktit'],
    'INTERDEPOSITOS': ['interdepositos'],
    'DEPOSITOS': ['deposito', 'depositos']
}

uncategorized = {}
total_procesados = 0

for pdf_path in pdfs:
    print(f"\n--- Analizando: {os.path.basename(pdf_path)} ---")
    transactions = extract_transactions_from_pdf(pdf_path)
    if not transactions:
        print("No se encontraron transacciones.")
        continue
    
    total_procesados += len(transactions)
    for t in transactions:
        detalle = t['DETALLE'] or ""
        detalle_norm = re.sub(r'[^a-z0-9]', '', detalle.lower())
        
        categorizado = False
        for cat, keywords in reglas_categorias.items():
            if any(kw in detalle_norm for kw in keywords):
                categorizado = True
                break
                
        if not categorizado:
            if detalle not in uncategorized:
                uncategorized[detalle] = 0
            uncategorized[detalle] += 1

print(f"\nTotal de transacciones procesadas: {total_procesados}")
if uncategorized:
    print("Transacciones que caen en 'OTROS' (No categorizadas):")
    for det, count in sorted(uncategorized.items(), key=lambda x: x[1], reverse=True):
        print(f" - {det} ({count} veces)")
else:
    print("¡Todas las transacciones fueron categorizadas correctamente!")
