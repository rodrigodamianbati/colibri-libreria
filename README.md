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

La paleta №79 y su versión aclarada están propuestas en Stitch. **No se copiaron al boceto local**. La última versión remota usa una imagen de ejemplo; el archivo real `colibri2.jpg` se conserva en el repositorio y en la vista local.

Las credenciales de Stitch no forman parte del repositorio. El inventario Excel original tampoco se incluye en este guardado del boceto.
