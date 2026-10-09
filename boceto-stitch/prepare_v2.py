import html
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).parent
shutil.copyfile(ROOT.parent / 'colibri2.jpg', ROOT / 'colibri2.jpg')
LISTS = ['Géneros', 'Subcategorías', 'Editoriales', 'Formatos', 'Ubicaciones', 'Estados', 'Idiomas']
styles = '''
<style>
html { color-scheme: dark; }
body { background:radial-gradient(ellipse at 78% 18%,#942b8855,transparent 55%),radial-gradient(ellipse at 15% 72%,#396ad333,transparent 50%),linear-gradient(135deg,#31105a,#5b1b7b 58%,#83267e)!important; }
.colibri-nav { position:relative;z-index:60;display:flex;align-items:center;gap:28px;padding:16px 4%;background:#240c44db;border-bottom:1px solid #e9baff25;font:14px Inter,Arial,sans-serif;color:#f4e8fc; }
.colibri-brand {display:flex;align-items:center;gap:12px;margin-right:12px;font:700 25px Georgia,serif;color:#fff;text-decoration:none;}
.colibri-brand img {width:32px;height:34px;object-fit:cover;object-position:50% 52%;border-radius:5px;}
.colibri-nav-link { color:#e6cdf6;text-decoration:none; padding:10px 0;white-space:nowrap; }
.colibri-nav-link.active {color:#fff;box-shadow:0 2px #eaa2fa;}
.colibri-admin {position:relative;}
.colibri-admin summary {cursor:pointer;padding:10px 0;list-style:none;}
.colibri-admin summary::after {content:' ▾';color:#df9eee;}
.colibri-admin-panel {position:absolute;top:100%;left:0;min-width:200px;background:#442062;border:1px solid #b782cc66;box-shadow:0 12px 30px #18052966;padding:8px;border-radius:12px;}
.colibri-admin-panel a {display:block;padding:10px 12px;text-decoration:none;color:#f2e2ff;border-radius:7px;}
.colibri-admin-panel a:hover {background:#733296;}
.colibri-add {margin-left:auto;background:linear-gradient(105deg,#7331d4,#a522a7);border:1px solid #db8ce366;border-radius:9px;color:#fff;padding:10px 17px;text-decoration:none;font-weight:600;white-space:nowrap;}
.bg-white {background-color:#f0e2fa!important;}
.preview-route-bar {position:relative;z-index:30;display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:0 auto 18px;padding:7px;background:#301346bb;border:1px solid #c69cdd55;border-radius:12px;width:max-content;max-width:calc(100% - 28px);font:12px Inter,Arial,sans-serif;}
.preview-route-bar a {color:#ebd9ff;text-decoration:none;padding:7px 10px;border-radius:7px;}
.preview-route-bar a.active {background:#8c36ad;color:white;}
@media(max-width:700px){.colibri-nav{gap:14px;padding:12px 18px;flex-wrap:wrap;}.colibri-brand{font-size:22px;}.colibri-add{padding:8px 11px;}.colibri-nav-link{font-size:13px;}.colibri-admin{font-size:13px;}}
</style>
'''

for name in ('inicio', 'resultados', 'libro', 'listas'):
    text = (ROOT / f'v2-{name}.html').read_text(encoding='utf-8')
    text = re.sub(r'(<img\b[^>]*\bsrc=)([\"\x27])(.*?)\2', lambda m: m[1] + m[2] + 'colibri2.jpg' + m[2], text, flags=re.S)
    text = re.sub(r'<body\b', f'<body data-preview-page="{name}"', text, count=1)
    admin = ''.join(f'<a href="listas-preview.html?lista={label}">{label}</a>' for label in LISTS)
    navbar = '<header class="colibri-nav"><a class="colibri-brand" href="inicio-preview.html"><img src="colibri2.jpg" alt="Logo CoLibri"><span>CoLibri</span></a>'
    navbar += f'<a class="colibri-nav-link {"active" if name == "inicio" else ""}" href="inicio-preview.html">Inicio</a>'
    navbar += f'<a class="colibri-nav-link {"active" if name == "resultados" else ""}" href="resultados-preview.html">Libros</a>'
    navbar += f'<details class="colibri-admin"><summary>Administración</summary><div class="colibri-admin-panel">{admin}</div></details>'
    navbar += '<a class="colibri-add" href="libro-preview.html">+ Agregar libro</a></header>'
    text = re.sub(r'<header\b.*?</header>', lambda _: navbar, text, count=1, flags=re.S)
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
