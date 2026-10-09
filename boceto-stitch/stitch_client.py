import json
import pathlib
import sys
import tomllib
import urllib.request

ROOT = pathlib.Path(__file__).parent

def call(name, arguments):
    with open(r'C:\Users\Bati\.codex\config.toml', 'rb') as f:
        config = tomllib.load(f)['mcp_servers']['stitch']
    headers = dict(config['http_headers'])
    headers.update({'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'})
    body = {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': name, 'arguments': arguments}}
    request = urllib.request.Request(config['url'], data=json.dumps(body).encode(), headers=headers)
    with urllib.request.urlopen(request, timeout=600) as response:
        raw = response.read().decode()
    data = json.loads(raw) if raw.lstrip().startswith('{') else next(json.loads(line[5:].strip()) for line in raw.splitlines() if line.startswith('data:'))
    if 'error' in data:
        raise RuntimeError(json.dumps(data['error']))
    return data['result']

if __name__ == '__main__':
    name, args_file, output_file = sys.argv[1:]
    result = call(name, json.loads(pathlib.Path(args_file).read_text(encoding='utf-8')))
    pathlib.Path(output_file).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    data = result.get('structuredContent') or json.loads(result['content'][0]['text'])
    summary = {'projectId': data.get('projectId'), 'name': data.get('name'), 'isError': result.get('isError', False)}
    summary['screens'] = [{k: v for k, v in screen.items() if k in ('name', 'id', 'title', 'screenshot', 'htmlCode', 'screenMetadata')}
        for component in data.get('outputComponents', []) for screen in component.get('design', {}).get('screens', [])]
    summary['text'] = [component.get('text') for component in data.get('outputComponents', []) if component.get('text')]
    print(json.dumps(summary, ensure_ascii=True))
