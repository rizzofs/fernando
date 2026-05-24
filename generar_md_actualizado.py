import os
import glob
import re

from generador_recovered import extract_transactions_from_pdf

pdf_dir = r"C:\Users\rizzo\Desktop\bancofer"
pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))

reglas_categorias = {
    'IMPUESTOS DEB/CRED': ['gravamenley25413sdeb', 'gravamenley25413scred'],
    'IVA DEBITO': ['ivabase'],
    'COMISIONES Y GASTOS': ['comispservrecaudacion', 'comispserv', 'comis', 'serv', 'comistransfne24'],
    'INTERDEPOSITOS': ['interdepositos', 'crtrasfinterbaneres'],
    'DEPOSITOS': ['deposito', 'depositos']
}

uncategorized = {}

for pdf_path in pdfs:
    transactions = extract_transactions_from_pdf(pdf_path)
    if not transactions:
        continue
    
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

out_path = r'C:\Users\rizzo\.gemini\antigravity-cli\brain\ef9699e9-3073-49c6-b5f4-5c458bbb576a\transacciones_no_categorizadas.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('# Transacciones No Categorizadas\n\n')
    f.write('Estas son todas las transacciones encontradas en los 18 PDFs que **NO** encajan en ninguna de las 5 categorías oficiales (`IMPUESTOS DEB/CRED`, `IVA DEBITO`, `COMISIONES Y GASTOS`, `INTERDEPOSITOS`, `DEPOSITOS`).\n\n')
    
    f.write('Actualmente, el programa no las incluye en la tabla "Resumen por Categoría". Si deseas que alguna de estas empiece a contabilizarse en una de las 5 categorías, avísame.\n\n')
    
    from collections import defaultdict
    grupos = defaultdict(int)
    for det, count in uncategorized.items():
        if det.startswith('DEBIN'):
            grupos['DEBIN (Múltiples CUITs)'] += count
        elif 'TRANS' in det or 'TR.' in det or 'TR ' in det or 'TRANSFERENCIA' in det:
            grupos['TRANSFERENCIAS (' + det + ')'] += count
        elif 'PAGO' in det:
            grupos['PAGOS (' + det + ')'] += count
        elif 'DEP.' in det or 'DEP ' in det or 'CH.' in det:
            grupos['CHEQUES Y DEPOSITOS (' + det + ')'] += count
        else:
            grupos['OTROS (' + det + ')'] += count
            
    for key, count in sorted(grupos.items(), key=lambda x: x[1], reverse=True):
        f.write(f'- `{key}` (Aparece {count} veces)\n')
