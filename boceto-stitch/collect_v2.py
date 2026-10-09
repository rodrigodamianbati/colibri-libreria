import json
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).parent
for filename in sys.argv[1:]:
    result = json.loads((ROOT / filename).read_text(encoding='utf-8'))
    data = result.get('structuredContent') or json.loads(result['content'][0]['text'])
    screens = [screen for component in data.get('outputComponents', []) for screen in component.get('design', {}).get('screens', [])]
    for screen in screens:
        title = screen.get('title', '')
        key = 'listas' if 'Editorial' in title or 'Administraci' in title else 'libro' if 'Nuevo' in title or 'Ficha' in title else 'resultados' if 'Resultado' in title or 'Listado' in title or 'Libros' in title and 'Inicio' not in title else 'inicio'
        (ROOT / f'v2-{key}-screen.json').write_text(json.dumps(screen, ensure_ascii=False, indent=2), encoding='utf-8')
        for prop, suffix in [('htmlCode', 'html'), ('screenshot', 'png')]:
            file = screen.get(prop, {})
            if file.get('downloadUrl'):
                urllib.request.urlretrieve(file['downloadUrl'], ROOT / f'v2-{key}.{suffix}')
        print(json.dumps({'screen': key, 'title': title, 'name': screen.get('name')}, ensure_ascii=True))
