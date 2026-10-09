# Acuerdos actuales · CoLibri

Estado guardado el 9 de octubre de 2026. Estos acuerdos simplifican el documento DISENO.md, que aún no fue actualizado.

## Libros y stock

- Cada registro representa un título; stock indica la cantidad de ejemplares. No se registra cada ejemplar por separado.
- Título y autor/a son campos separados.
- Todos los campos son obligatorios por ahora: título, autor/a, editorial, género, subcategoría, descripción breve, formato, año, idioma, ubicación, estado, precio de venta y stock.
- Solo se guarda precio de venta. No se guarda ISBN ni precio de costo.
- Género y subcategoría son catálogos independientes, sin jerarquía. Cada título tiene uno de cada uno por ahora.
- Stock de un alta nueva: 0 por defecto, editable por el usuario.
- La carga inicial se basará en el Excel. Los valores 0 detectados en ese inventario fueron un error y deben interpretarse como 1 durante esa carga; esto no cambia el valor por defecto de las altas nuevas.
- No hay baja de libros por ahora. El usuario puede dejar stock en 0.
- Fechas automáticas de alta y modificación. Las fechas de venta pertenecen al historial de ventas.

## Catálogos editables

CRUD para géneros, subcategorías, editoriales, formatos, ubicaciones, estados e idiomas. El usuario podrá redefinir estas listas posteriormente.

Estados iniciales: Disponible, Vendido, Pedir y En espera.

El boceto ilustra Editoriales. El comportamiento de eliminación de elementos de catálogo que ya están en uso queda pendiente de definición final.

## Pantallas

- Navegación superior con Inicio, Libros, Administración y Agregar libro.
- Inicio: logo grande centrado arriba, buscador amplio y filtros debajo; sin listado de libros.
- Buscar o presionar Enter abre Libros/Resultados, conservando la consulta y los filtros.
- Libros conserva el listado/tablas y filtros del boceto anterior.
- Nuevo libro muestra todos los campos obligatorios y stock inicial 0.
- Administración permite acceder a los siete catálogos independientes.
- La vista local usa el logo real colibri2.jpg. Las pantallas de Stitch pueden usar una imagen de ejemplo, autorizada por el usuario al no estar disponible la carga de imagen mediante MCP.

## Colores y aplicación local

Paleta elegida: https://paletasdecolores.com/paleta-de-colores-79/.

| Color | HEX original |
|---|---|
| Violeta | #6f4b93 |
| Verde oliva oscuro | #405326 |
| Lima oliva claro | #d7e37f |
| Malva rosado | #bd8aab |
| Malva oscuro | #885775 |

Se pidió aclarar solo un poco los violetas y verdes. Stitch generó cuatro versiones refinadas y reportó violeta #7c589e y verde oliva #4c6130, con lima #d7e37f / #e2ec98.

El usuario considera que Stitch no reprodujo exactamente lo buscado, aunque el resultado sirve como referencia. El estado anterior se guardó en Git antes de copiar las pantallas.

Posteriormente se incorporaron las cuatro pantallas de Stitch a la vista local, aclarando más los fondos violetas y verdes porque aún resultaban demasiado oscuros: violeta base #9875b1, gradiente hacia #ab8bbf y #bc99b5, verde de acciones #91a664 y texto oscuro #263515. El logo real colibri2.jpg reemplaza la imagen de ejemplo. Se mantiene la búsqueda con filtros y el stock de alta en 0.
