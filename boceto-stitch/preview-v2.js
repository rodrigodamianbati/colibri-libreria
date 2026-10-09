(() => {
  const page = document.body.dataset.previewPage;
  const targets = { Inicio: 'inicio-preview.html', Libros: 'resultados-preview.html', Administración: 'listas-preview.html' };
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const label = element => element.textContent.replace(/arrow_drop_down|keyboard_arrow_down|expand_more|chevron_right|chevron_left|add|search|edit|arrow_back/g, '').trim();
  document.querySelectorAll('header a, nav a').forEach(a => {
    const name = label(a);
    if (targets[name]) a.href = targets[name];
  });
  document.querySelectorAll('button,a').forEach(control => {
    const text = label(control);
    if (/Agregar libro/.test(text)) control.addEventListener('click', event => { event.preventDefault(); location.href = 'libro-preview.html'; });
    if (/Volver al inicio/.test(text)) control.addEventListener('click', event => { event.preventDefault(); location.href = 'inicio-preview.html'; });
    if (/Volver a libros|Volver al catálogo/.test(text)) control.addEventListener('click', event => { event.preventDefault(); location.href = 'resultados-preview.html'; });
    if (text === 'Administración') control.addEventListener('click', event => { event.preventDefault(); location.href = 'listas-preview.html'; });
  });
  if (page !== 'inicio' && page !== 'resultados') return;

  const input = document.querySelector('main input[type="search"],main input[type="text"],main input:not([type])');
  const filters = [...document.querySelectorAll('main select')].slice(0, 4);
  const keys = ['genero', 'subcategoria', 'editorial', 'estado'];
  const initial = new URLSearchParams(location.search);
  if (input) input.value = initial.get('q') || '';
  filters.forEach((select, i) => {
    const value = initial.get(keys[i]);
    const option = value && [...select.options].find(o => normalize(o.textContent.trim()) === normalize(value));
    if (option) select.value = option.value;
    else select.selectedIndex = 0;
  });
  const values = () => {
    const query = new URLSearchParams();
    const q = input?.value.trim();
    if (q) query.set('q', q);
    filters.forEach((select, i) => {
      const option = select.options[select.selectedIndex];
      if (select.selectedIndex > 0 && option) query.set(keys[i], option.textContent.trim());
    });
    return query;
  };
  const search = () => {
    const query = values().toString();
    location.href = 'resultados-preview.html' + (query ? '?' + query : '');
  };
  input?.addEventListener('keydown', event => { if (event.key === 'Enter') { event.preventDefault(); search(); } });
  document.querySelectorAll('main form').forEach(form => form.addEventListener('submit', event => { event.preventDefault(); search(); }));
  document.querySelectorAll('main button').forEach(button => {
    const text = label(button);
    if (text === 'Buscar') button.addEventListener('click', event => { event.preventDefault(); search(); });
    if (/Limpiar/.test(text)) button.addEventListener('click', event => { event.preventDefault(); if (input) input.value = ''; filters.forEach(s => s.selectedIndex = 0); if (page === 'resultados') search(); });
  });
  if (page !== 'resultados') return;

  const books = [
    { titulo: 'El profeta', autor: 'Gibran Khalil Gibran', editorial: 'Kier', precio: '$ 18.500,00', genero: 'Religión & espiritualidad', subcategoria: 'Ensayo', estado: 'Disponible' },
    { titulo: 'El día que apagaron la luz', autor: 'Camila Fabri', editorial: 'Seix Barral', precio: '$ 24.000,00', genero: 'Novela', subcategoria: 'Contemporánea', estado: 'Disponible' },
    { titulo: 'El coleccionista', autor: 'Nora Roberts', editorial: 'Debolsillo', precio: '$ 21.500,00', genero: 'Novela', subcategoria: 'Ficción', estado: 'Disponible' },
    { titulo: 'Cuba Stone, tres historias', autor: 'Javier Sinay, Joselo y Jeremías Gamboa', editorial: 'Tusquets', precio: '$ 19.800,00', genero: 'Crónica', subcategoria: 'No ficción', estado: 'Disponible' }
  ];
  const q = normalize(initial.get('q') || '');
  const matching = books.filter(book => normalize(book.titulo + ' ' + book.autor).includes(q) && keys.every(key => !initial.has(key) || normalize(book[key]) === normalize(initial.get(key))));
  const tbody = document.querySelector('main table tbody');
  if (tbody) {
    const template = tbody.querySelector('tr');
    tbody.replaceChildren();
    matching.forEach(book => {
      const row = template?.cloneNode(true) || document.createElement('tr');
      const cells = [...row.querySelectorAll('td')];
      if (cells.length >= 7) {
        [book.titulo, book.autor, book.editorial, book.precio, '1', book.estado].forEach((value, i) => { cells[i].textContent = value; cells[i].style.color = '#3b176b'; });
        cells[6].replaceChildren();
        const action = document.createElement('a');
        action.href = 'libro-preview.html'; action.textContent = 'Editar';
        action.style.cssText = 'display:inline-block;padding:7px 13px;border:1px solid #a786ce;border-radius:8px;color:#632191;background:#f0ddfa;font-weight:600;text-decoration:none';
        cells[6].append(action);
      }
      tbody.append(row);
    });
    if (!matching.length) {
      const row = document.createElement('tr');
      const cell = document.createElement('td');
      cell.colSpan = 7;
      cell.style.cssText = 'padding:44px;text-align:center;color:#4c236f';
      cell.textContent = 'No encontramos libros con esa búsqueda. Probá con otro título, autor/a o filtros.';
      row.append(cell); tbody.append(row);
    }
  }
  const context = document.createElement('div');
  context.style.cssText = 'margin:18px 0;color:#30213e;font:14px Inter,sans-serif';
  context.textContent = `${matching.length} ${matching.length === 1 ? 'título' : 'títulos'} · ${matching.length} ${matching.length === 1 ? 'ejemplar' : 'ejemplares'}` + (initial.get('q') ? ` · Búsqueda: «${initial.get('q')}»` : ' · Todos los libros') + ' · Datos de ejemplo';
  document.querySelector('main table')?.closest('section')?.before(context);
  // Replace static example counters with counts for the actual displayed sample.
  document.querySelectorAll('main span,main p,main div').forEach(element => {
    if (element.children.length) return;
    const text = element.textContent.trim();
    if (/^\d+ títulos?\s*[·•]\s*\d+ ejemplares?$/.test(text)) element.textContent = `${matching.length} ${matching.length === 1 ? 'título' : 'títulos'} · ${matching.length} ${matching.length === 1 ? 'ejemplar' : 'ejemplares'}`;
    if (/^\d+ títulos? coincidentes$/.test(text)) element.textContent = `${matching.length} ${matching.length === 1 ? 'título coincidente' : 'títulos coincidentes'}`;
    if (/^\d+ títulos?$/.test(text)) element.textContent = `${matching.length} ${matching.length === 1 ? 'título' : 'títulos'}`;
    if (/^\d+ ejemplares?$/.test(text)) element.textContent = `${matching.length} ${matching.length === 1 ? 'ejemplar' : 'ejemplares'}`;
    if (/^Mostrando \d/.test(text)) element.textContent = matching.length ? `Mostrando 1–${matching.length} de ${matching.length} libros` : 'Sin resultados';
  });
})();
