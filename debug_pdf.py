import re
import os
from generador_recovered import extract_transactions_from_pdf

reglas_categorias = {
    'IMPUESTOS DEB/CRED': ['gravamenley25413sdeb', 'gravamenley25413scred', 'reintegroley25413deb', 'reintegroley25413cred', 'vsgytley25413'],
    'IVA DEBITO': ['ivabase'],
    'COMISIONES Y GASTOS': ['comistransfne24', 'comiscompensacionatenc'],
    'INTERDEPOSITOS': [
        'debtraninterblink', 'debtraninterblinkres', 'pagovepafip', 'pagoedensa', 
        'dbcredintranslinkcia', 'debitopagodirecto', 'pagomovistar', 'pagomovistarhogar', 
        'pagocajademedaportp', 'pagofaecys'
    ],
    'DEPOSITOS': [
        'debtraninterblinktit', 'rendpservrecaudacion', 'transfintdistlinklar', 
        'cbetrobcodsuc0001k', 'rendicionpagoslink', 'debin', 'transfintdistbanelar', 
        'crtrvariosvsuc0001', 'crtransfinterlinkres', 'dep', 'deposito', 'efectivo', 'ch',
        'transfintermmlinkular', 'camfeddistpzaobcos', '48hsbancos', 'crtransfinterbaneres',
        'creditosvarios', 'cobradoporcaja', 'crtrfacturasuc0001'
    ]
}

pdf_path = r"C:\Users\rizzo\Desktop\bancofer\18Estado de Cuenta Abril 2026.pdf"
transactions = extract_transactions_from_pdf(pdf_path)

print(f"Total transactions extracted: {len(transactions)}")

first_t = transactions[0]
starting_saldo = first_t['SALDO'] + float(first_t['DEBITOS']) - float(first_t['CREDITOS'])
print(f"Computed Starting Saldo: {starting_saldo}")

resumen = {cat: {'debitos': 0.0, 'creditos': 0.0} for cat in reglas_categorias}
resumen['NO_CATEGORIZADO'] = {'debitos': 0.0, 'creditos': 0.0}

for t in transactions:
    detalle = t['DETALLE'] or ""
    detalle_norm = re.sub(r'[^a-z0-9]', '', detalle.lower())
    debito = float(t['DEBITOS'])
    credito = float(t['CREDITOS'])
    
    categorizado = False
    for cat, keywords in reglas_categorias.items():
        if any(kw in detalle_norm for kw in keywords):
            resumen[cat]['debitos'] += debito
            resumen[cat]['creditos'] += credito
            categorizado = True
            break
            
    if not categorizado:
        resumen['NO_CATEGORIZADO']['debitos'] += debito
        resumen['NO_CATEGORIZADO']['creditos'] += credito
        print(f"NO CAT: {detalle} | Debito: {debito} | Credito: {credito}")

print("\n--- RESUMEN ---")
for cat, vals in resumen.items():
    print(f"{cat}: DEB={vals['debitos']} | CRED={vals['creditos']}")

calc = starting_saldo 
calc -= resumen['IMPUESTOS DEB/CRED']['debitos']
calc -= resumen['IVA DEBITO']['debitos']
calc -= resumen['COMISIONES Y GASTOS']['debitos']
calc -= resumen['INTERDEPOSITOS']['debitos']
calc += resumen['DEPOSITOS']['creditos']

print(f"\nUser Formula calculated balance: {calc}")
print(f"Actual final balance in PDF: {transactions[-1]['SALDO']}")
