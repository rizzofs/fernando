import os
import glob
import re
from collections import defaultdict

from generador_recovered import extract_transactions_from_pdf

pdf_dir = r"C:\Users\rizzo\Desktop\bancofer"
pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))

reglas_categorias = {
    'IMPUESTOS DEB/CRED': ['gravamenley25413sdeb', 'gravamenley25413scred'],
    'IVA DEBITO': ['ivabase'],
    'COMISIONES Y GASTOS': ['comispservrecaudacion', 'comispserv', 'comis', 'serv', 'comistransfne24', 'comiscompensacionatenc'],
    'INTERDEPOSITOS': [
        'debtraninterblink', 'debtraninterblinkres', 'pagovepafip', 'pagoedensa', 
        'dbcredintranslinkcia', 'debitopagodirecto', 'pagomovistar', 'pagomovistarhogar', 
        'pagocajademedaportp', 'pagofaecys'
    ],
    'DEPOSITOS': [
        'debtraninterblinktit', 'rendpservrecaudacion', 'transfintdistlinklar', 
        'cbetrobcodsuc0001k', 'rendicionpagoslink', 'debin', 'transfintdistbanelar', 
        'crtrvariosvsuc0001', 'crtransfinterlinkres', 'dep', 'deposito', 'efectivo', 'ch'
    ]
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

agrupado = defaultdict(list)
for det, count in uncategorized.items():
    if det.startswith('DEBIN'):
        agrupado['DEBINES'].append((det, count))
    elif 'TRANS' in det or 'TR.' in det or 'TR ' in det or 'TRANSFERENCIA' in det:
        agrupado['TRANSFERENCIAS'].append((det, count))
    elif 'PAGO' in det:
        agrupado['PAGOS'].append((det, count))
    elif 'DEP.' in det or 'DEP ' in det or 'CH.' in det or 'CHEQUE' in det:
        agrupado['CHEQUES Y DEPOSITOS EXTRA'].append((det, count))
    else:
        agrupado['OTROS'].append((det, count))

out_path = r'C:\Users\rizzo\.gemini\antigravity-cli\brain\ef9699e9-3073-49c6-b5f4-5c458bbb576a\transacciones_no_categorizadas.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('# Transacciones No Categorizadas (Agrupadas)\n\n')
    f.write('Estas son todas las transacciones encontradas en los 18 PDFs que **NO** encajan en las reglas actuales del programa. Están agrupadas lógicamente para facilitar su revisión.\n\n')
    
    for macro_cat, items in sorted(agrupado.items()):
        f.write(f'## {macro_cat}\n')
        # Sort items by count descending
        for det, count in sorted(items, key=lambda x: x[1], reverse=True):
            f.write(f'- `{det}` ({count} veces)\n')
        f.write('\n')

print("Artifact actualizado con éxito.")
