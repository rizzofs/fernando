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

# Dict to store the mapping: Categoria -> Dict[Detalle, Count]
resultados = {
    'IMPUESTOS DEB/CRED': defaultdict(int),
    'IVA DEBITO': defaultdict(int),
    'COMISIONES Y GASTOS': defaultdict(int),
    'INTERDEPOSITOS': defaultdict(int),
    'DEPOSITOS': defaultdict(int),
    'NO CATEGORIZADAS': defaultdict(int)
}

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
                resultados[cat][detalle] += 1
                categorizado = True
                break
                
        if not categorizado:
            resultados['NO CATEGORIZADAS'][detalle] += 1

out_path = r'C:\Users\rizzo\.gemini\antigravity-cli\brain\ef9699e9-3073-49c6-b5f4-5c458bbb576a\transacciones_no_categorizadas.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('# Reporte Completo de Categorías\n\n')
    f.write('A continuación te listo TODAS las transacciones encontradas en los 18 PDFs, organizadas exactamente por la categoría a la que pertenecen actualmente (con las reglas originales del binario).\n\n')
    f.write('Al final verás las "NO CATEGORIZADAS". Puedes indicarme libremente qué transacciones mover de un lado a otro o en qué categoría incluir las nuevas.\n\n')
    
    for cat in ['IMPUESTOS DEB/CRED', 'IVA DEBITO', 'COMISIONES Y GASTOS', 'INTERDEPOSITOS', 'DEPOSITOS', 'NO CATEGORIZADAS']:
        f.write(f'## {cat}\n')
        items = resultados[cat]
        if not items:
            f.write('- *(Ninguna transacción)*\n\n')
        else:
            for det, count in sorted(items.items(), key=lambda x: x[1], reverse=True):
                f.write(f'- `{det}` ({count} veces)\n')
            f.write('\n')

print("Artifact actualizado con todas las categorías.")
