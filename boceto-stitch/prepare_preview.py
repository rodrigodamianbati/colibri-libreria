import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
logo = 'data:image/jpeg;base64,' + base64.b64encode((ROOT.parent / 'colibri.jpg').read_bytes()).decode()

for name in ('inicio', 'libro', 'listas'):
    source = ROOT / f'{name}.html'
    text = source.read_text(encoding='utf-8')
    text = re.sub(r'(<img\b[^>]*\bsrc=)([\"\x27])(.*?)\2', lambda m: m[1] + m[2] + logo + m[2], text, flags=re.S)
    text = text.replace('object-cover rounded-lg', 'object-contain rounded-lg')
    def correct_state(match):
        block = match.group(0)
        if 'Agotado' not in block and 'En Reserva' not in block:
            return block
        opening = block[:block.index('>') + 1]
        return opening + '<option value="">Estado (Todos)</option>' + ''.join(f'<option>{state}</option>' for state in ('Disponible', 'Vendido', 'Pedir', 'En espera')) + '</select>'
    text = re.sub(r'<select\b.*?</select>', correct_state, text, flags=re.S)
    # Preview navigation is intentionally separate from the application mockup.
    toolbar = '<div style="position:fixed;bottom:16px;left:50%;transform:translateX(-50%);z-index:9999;display:flex;gap:6px;padding:7px;background:#ffffffee;border:1px solid #ddd6fe;border-radius:12px;box-shadow:0 4px 16px #2e10651a;font:13px Inter,sans-serif">'
    for label, target in [('Inicio', 'inicio'), ('Ficha del libro', 'libro'), ('Administrar listas', 'listas')]:
        selected = 'background:#6d28d9;color:white;' if target == name else 'color:#5b21b6;'
        toolbar += f'<a style="padding:8px 12px;border-radius:7px;text-decoration:none;{selected}" href="{target}-preview.html">{label}</a>'
    toolbar += '</div>'
    text = text.replace('</body>', toolbar + '</body>')
    (ROOT / f'{name}-preview.html').write_text(text, encoding='utf-8')
print('Tres vistas previas preparadas con el logo original.')
