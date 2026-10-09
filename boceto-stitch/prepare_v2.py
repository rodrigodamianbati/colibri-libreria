import html
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).parent
shutil.copyfile(ROOT.parent / 'colibri2.jpg', ROOT / 'colibri2.jpg')
shutil.copyfile(ROOT.parent / 'colibri-largo.jpeg', ROOT / 'colibri-largo.jpeg')
LISTS = ['Géneros', 'Subcategorías', 'Editoriales', 'Formatos', 'Ubicaciones', 'Estados', 'Idiomas']
styles = '<link rel="stylesheet" href="paleta-local.css">'
# Stitch source colors are preserved in refinada-*.html; only previews are lightened.
LIGHTER = {
    '#4d632f': '#91a664', '#4c6130': '#91a664', '#526932': '#91a664',
    '#597437': '#a5b97b', '#405326': '#819452',
    '#482866': '#76548f', '#42225f': '#76548f',
    '#7d57a2': '#9875b1', '#7c589e': '#9875b1',
    '#563970': '#80608f', '#5a3c75': '#80608f',
}

for name in ('inicio', 'resultados', 'libro', 'listas'):
    text = (ROOT / f'refinada-{name}.html').read_text(encoding='utf-8')
    for original, lighter in LIGHTER.items():
        text = re.sub(re.escape(original), lighter, text, flags=re.I)
    text = re.sub(r'(<img\b[^>]*\bsrc=)([\"\x27])(.*?)\2', lambda m: m[1] + m[2] + 'colibri2.jpg' + m[2], text, flags=re.S)
    text = re.sub(r'<body\b', f'<body data-preview-page="{name}"', text, count=1)
    admin = ''.join(f'<a href="listas-preview.html?lista={label}">{label}</a>' for label in LISTS)
    navbar = '<header class="colibri-nav"><a class="colibri-brand" href="inicio-preview.html"><img src="colibri2.jpg" alt="Logo CoLibri"><span>CoLibri</span></a>'
    navbar += f'<a class="colibri-nav-link {"active" if name == "inicio" else ""}" href="inicio-preview.html">Inicio</a>'
    navbar += f'<a class="colibri-nav-link {"active" if name == "resultados" else ""}" href="resultados-preview.html">Libros</a>'
    navbar += f'<details class="colibri-admin"><summary>Administración</summary><div class="colibri-admin-panel">{admin}</div></details>'
    navbar += '<a class="colibri-add" href="libro-preview.html">+ Agregar libro</a></header>'
    text = re.sub(r'<header\b.*?</header>', lambda _: navbar, text, count=1, flags=re.S)
    if name == 'inicio':
        text = text.replace('w-[460px] max-w-[92vw] h-[330px]', 'colibri-hero-wide')
        text = re.sub(r'(<main\b.*?)(</main>)', lambda match: match[1].replace('src="colibri2.jpg"', 'src="colibri-largo.jpeg"') + match[2], text, flags=re.S)
    if name in ('inicio', 'resultados'):
        text = re.sub(r'\s+onsubmit="[^"]*"', '', text)
        # Keep the search filter options consistent with the illustrative records.
        groups = [
            ('Género (Todos)', ['Religión & espiritualidad', 'Novela', 'Crónica', 'Poesía']),
            ('Subcategoría (Todos)', ['Ensayo', 'Contemporánea', 'Ficción', 'No ficción']),
            ('Editorial (Todas)', ['Kier', 'Seix Barral', 'Debolsillo', 'Tusquets']),
            ('Estado (Todos)', ['Disponible', 'Vendido', 'Pedir', 'En espera'])
        ]
        count = [0]
        def select_options(match):
            if count[0] >= 4:
                return match.group(0)
            placeholder, options = groups[count[0]]
            count[0] += 1
            opening = match.group(0).split('>', 1)[0] + '>'
            return opening + f'<option value="">{placeholder}</option>' + ''.join(f'<option value="{html.escape(value, quote=True)}">{html.escape(value)}</option>' for value in options) + '</select>'
        text = re.sub(r'<select\b.*?</select>', select_options, text, flags=re.S)
    text = text.replace('</head>', styles + '</head>')
    toolbar = '<div class="preview-route-bar" aria-label="Vistas del boceto">'
    for label, target in [('Inicio', 'inicio'), ('Libros', 'resultados'), ('Ficha del libro', 'libro'), ('Administrar listas', 'listas')]:
        toolbar += f'<a class="{"active" if name == target else ""}" href="{target}-preview.html">{label}</a>'
    toolbar += '</div><script src="preview-v2.js"></script>'
    text = text.replace('</body>', toolbar + '</body>')
    (ROOT / f'{name}-preview.html').write_text(text, encoding='utf-8')
print('Cuatro vistas actualizadas con colibri2.jpg y navegación de búsqueda.')
