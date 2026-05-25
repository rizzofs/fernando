import re
import os
from generador_recovered import extract_transactions_from_pdf

reglas_categorias = {
    'IMPUESTOS DEB/CRED': ['gravamenley25413sdeb', 'gravamenley25413scred', 'reintegroley25413deb', 'reintegroley25413cred', 'vsgytley25413'],
    'IVA DEBITO': ['ivabase'],
    'COMISIONES Y GASTOS': ['comispservrecaudacion', 'comispserv', 'comistransfne24', 'comiscompensacionatenc', 'comiscanjeobancos'],
    'CHEQUES DEBITADOS': ['pagochequepropiacasa'],
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

pdf_path = r"C:\Users\rizzo\Desktop\bancofer\17Estado de Cuenta Abril 2026 Pagos.pdf"
transactions = extract_transactions_from_pdf(pdf_path)

debitos_en_depositos = 0.0

print("Transacciones en DEPOSITOS que tienen DEBITOS:")
for t in transactions:
    detalle = t['DETALLE'] or ""
    detalle_norm = re.sub(r'[^a-z0-9]', '', detalle.lower())
    debito = float(t['DEBITOS'])
    
    # Check if it belongs to DEPOSITOS
    if debito > 0:
        if any(kw in detalle_norm for kw in reglas_categorias['DEPOSITOS']):
            # Wait, verify it didn't belong to a previous category first
            categorizado_antes = False
            for cat in ['IMPUESTOS DEB/CRED', 'IVA DEBITO', 'COMISIONES Y GASTOS', 'CHEQUES DEBITADOS', 'INTERDEPOSITOS']:
                if any(kw in detalle_norm for kw in reglas_categorias[cat]):
                    categorizado_antes = True
                    break
            
            if not categorizado_antes:
                print(f"- Detalle: {detalle} | Debito: {debito}")
                debitos_en_depositos += debito

print(f"\nSuma total de debitos en DEPOSITOS: {debitos_en_depositos}")
