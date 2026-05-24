import re
from collections import defaultdict
import json

with open('resultado_categorias.txt', encoding='utf-16le') as f:
    text = f.read()

matches = re.findall(r' - (.*?) \((\d+) veces\)', text)

grupos = defaultdict(int)
for det, count in matches:
    if det.startswith('DEBIN'):
        grupos['DEBIN (varios números y CUITs combinados)'] += int(count)
    elif 'TRANS' in det or 'TR.' in det or 'TR ' in det or 'TRANSFERENCIA' in det:
        grupos['TRANSFERENCIAS (' + det + ')'] += int(count)
    elif 'PAGO' in det:
        grupos['PAGOS (' + det + ')'] += int(count)
    elif 'DEP.' in det or 'DEP ' in det or 'CH.' in det:
        grupos['CHEQUES Y DEPOSITOS (' + det + ')'] += int(count)
    else:
        grupos['OTROS (' + det + ')'] += int(count)

out_path = r'C:\Users\rizzo\.gemini\antigravity-cli\brain\ef9699e9-3073-49c6-b5f4-5c458bbb576a\transacciones_no_categorizadas.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('# Transacciones No Categorizadas (Histórico de 18 PDFs)\n\n')
    f.write('Hemos analizado todos los PDFs de la carpeta `bancofer`. A continuación, se listan agrupadas las transacciones que el sistema manda a la categoría "OTROS".\n\n')
    f.write('Por favor indícame cómo agruparlas. Puedes asignarlas a categorías existentes o sugerir nuevas (ej. "PAGOS", "TRANSFERENCIAS RECIBIDAS").\n\n')
    
    for key, count in sorted(grupos.items(), key=lambda x: x[1], reverse=True):
        f.write(f'- `{key}` (Aparece {count} veces)\n')

print("Artifact actualizado.")
