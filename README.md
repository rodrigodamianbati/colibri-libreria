# CoLibri · Librería de Manu

Boceto de la gestión de libros y stock. Este repositorio guarda el trabajo de diseño previo a implementar la aplicación.

## Ver el boceto local

Con Python instalado, ejecutar desde la raíz del repositorio:

```powershell
python -m http.server 8765 --bind 127.0.0.1 --directory boceto-stitch
```

Abrir http://127.0.0.1:8765/inicio-preview.html.

Las cuatro pantallas son Inicio, Libros/Resultados, Nuevo libro y Administración/Editoriales. La búsqueda navega al listado y conserva los filtros. Los datos son ejemplos; los formularios no guardan información y todavía no hay base de datos.

El boceto usa Tailwind, fuentes y otros recursos externos: esta vista de diseño requiere conexión para cargarlos. La aplicación final prevista debe funcionar sin conexión.

## Estado guardado

- `boceto-stitch/`: vista local probada, logo, capturas, bocetos originales y pedidos/respuestas de Stitch.
- `docs/ACUERDOS.md`: reglas de negocio y decisiones actuales.
- `CONTEXTO.md`: contexto de arquitectura, con decisiones todavía pendientes.
- `DISENO.md`: documento de diseño previo; aún no refleja todas las simplificaciones acordadas. En caso de diferencias, consultar `docs/ACUERDOS.md`.
- `docs/stitch/`: respuesta de la última propuesta de colores aclarados.

Proyecto de Stitch: https://stitch.withgoogle.com/projects/13227700106738505093.

Las cuatro pantallas de la última versión de Stitch están incorporadas al boceto local. Sus fuentes se conservan en `boceto-stitch/refinada-*.html`. La vista local aclara aún más los violetas y verdes mediante `paleta-local.css`, con violeta base `#9875b1` y verde de acciones `#91a664`; los botones claros usan texto oscuro. La versión remota usa una imagen de ejemplo; la vista local usa el archivo real `colibri2.jpg`.

Para regenerar las cuatro vistas a partir de las fuentes de Stitch y los ajustes locales:

```powershell
python boceto-stitch/prepare_v2.py
```

El inicio usa `colibri-largo.jpeg` en un banner horizontal de hasta 840 px, con proporción 4:1 y ancho adaptable. La barra de navegación conserva `colibri2.jpg`.

Las credenciales de Stitch no forman parte del repositorio. El inventario Excel original tampoco se incluye en este guardado del boceto.
