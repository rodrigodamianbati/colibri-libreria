# Gestor de stock para librería: documento de diseño

> **Para quien lo lea (persona o IA):** este documento es la fuente de verdad del proyecto. Recoge todas las decisiones ya tomadas con el usuario. Lo marcado como **[A COMPLETAR]** está intencionalmente sin detallar y debe resolverse al implementar (siempre respetando los principios de la sección 2). No cambies decisiones cerradas sin consultarlo con el usuario.

---

## 1. Contexto y alcance

- **Qué es**: aplicación de escritorio para gestionar el stock de una librería de **libros nuevos** (cientos de títulos hoy, preparada para miles).
- **Dónde corre**: **una sola PC con Windows**, un solo usuario. Sin servidores, sin internet obligatorio.
- **Quién la desarrolla**: el usuario **no escribe ni toca código**. Todo se genera por conversación; el código debe ser fácil de leer, probar y modificar por iteraciones sucesivas.
- **País / moneda**: Argentina, peso argentino (ARS).
- **Funciones pedidas**: CRUD de libros, carga masiva por CSV, listado y búsqueda, ventas, entradas (compras), precio de venta y precio de compra mayorista, contabilidad básica, reportes.
- **Extras aceptados**: actualización masiva de precios, consignación, sugerencia de reposición, etiquetas imprimibles con código de barras, autocompletar metadatos por ISBN (opcional), devoluciones, encargos de clientes, copias de seguridad automáticas, registro de cambios (auditoría), conteo físico con lector.
- **Previsto para el futuro (diseñado pero no activo)**: IVA, facturación electrónica ARCA, varios usuarios con roles, lectores de códigos de barras e impresoras térmicas.

---

## 2. Principios de diseño (innegociables)

1. **Importes en enteros** (centavos de peso). Nunca `float` para dinero. Presentación: `$ 12.345,67`.
2. **El stock no se edita a mano**: se calcula/deriva de **movimientos**. Los ajustes también son movimientos, con motivo.
3. **Foto del momento**: cada línea de venta/compra guarda precio, costo, tasa de impuesto y moneda vigentes en ese instante. Cambios posteriores no alteran historia.
4. **Borrado lógico**: lo que tiene historial se desactiva, no se elimina.
5. **Inmutabilidad de documentos emitidos**: una venta confirmada o un comprobante emitido no se edita; se corrige con anulación, devolución o nota de crédito.
6. **Tres capas separadas**: interfaz (sin lógica), servicios (reglas de negocio), datos (SQLite). Los servicios deben poder probarse sin abrir ninguna ventana.
7. **Preparado para ampliar sin migraciones dolorosas**: las estructuras de impuestos, comprobantes, clientes, usuarios y permisos existen desde el inicio, aunque hoy estén con valores neutros.
8. **Migraciones versionadas** de base de datos desde el primer día.
9. **Transacciones**: toda operación compuesta (venta, compra, importación) entra completa o no entra.
10. **Seguridad de los datos**: el archivo `.db` es todo el negocio; copias de seguridad y verificación de integridad son parte del producto, no un extra.

---

## 3. Stack y entrega

| Aspecto | Decisión |
|---|---|
| Lenguaje | Python 3.11+ |
| Interfaz | PySide6 (Qt) |
| Base de datos | SQLite (archivo único, modo WAL, claves foráneas activas) |
| Reportes | openpyxl (Excel), reportlab (PDF) |
| Códigos de barras | librería para Code 128 / EAN-13 (p. ej. `python-barcode`) o dibujo con reportlab |
| Pruebas | pytest |
| Empaquetado | PyInstaller, `.exe` para Windows |

**Nota sobre el empaquetado:** PyInstaller solo genera `.exe` de Windows desde una máquina Windows (o CI con runner Windows, p. ej. GitHub Actions). Se entrega un `build.bat` de doble clic. El resto del desarrollo y las pruebas se pueden ejecutar fuera de Windows (lógica y base de datos; la interfaz con `QT_QPA_PLATFORM=offscreen`).

**Ubicación de datos:** carpeta del usuario (p. ej. `%APPDATA%\GestorLibreria\`) con `libreria.db`, `backups/`, `config.json`, `logs/`. Debe poder indicarse otra ruta (modo portable).

---

## 4. Arquitectura

```
gestor_libreria/
├─ app/
│  ├─ main.py                 # arranque
│  ├─ config.py               # rutas, ajustes
│  ├─ db/
│  │  ├─ connection.py        # conexión, PRAGMAs
│  │  ├─ migrations/          # 0001_inicial.sql, 0002_...
│  │  └─ repositories/        # acceso a datos por entidad
│  ├─ domain/                 # modelos, validadores (ISBN, CUIT), dinero
│  ├─ services/               # reglas de negocio
│  │  ├─ libros.py  stock.py  ventas.py  compras.py
│  │  ├─ importacion.py  precios.py  reportes.py
│  │  ├─ contabilidad.py  backup.py  auditoria.py  permisos.py
│  ├─ printing/               # ticket, etiquetas (interfaz + adaptadores)
│  ├─ ui/                     # ventanas, diálogos, widgets
│  └─ resources/              # plantillas CSV/XLSX, iconos
├─ tests/
├─ tools/                     # generador de datos sintéticos
├─ build.bat
└─ requirements.txt
```

- Las pantallas llaman a servicios; los servicios llaman a repositorios. La UI nunca ejecuta SQL.
- **Dinero**: tipo/utilidad única (`Dinero` o funciones de conversión) para parsear texto ("12.345,67" y "12345.67") y formatear. Prohibido operar con `float`.
- **Usuario actual**: los servicios reciben/consultan un "contexto" con el usuario actual (hoy siempre el administrador).
- **Permisos**: toda acción sensible pasa por `permisos.puede(usuario, accion)`, hoy siempre `True`.
- **Acceso a datos aislado** para poder cambiar de motor en el futuro si hiciera falta (varios puestos simultáneos por red exigirían un servidor de BD; SQLite no es adecuado para eso).

---

## 5. Modelo de datos

Convenciones: `id` entero autoincremental; `creado_en`, `modificado_en`, `creado_por`, `modificado_por` en tablas principales; importes en centavos (`INTEGER`); fechas en ISO 8601; `activo` para borrado lógico. **[A COMPLETAR]** el DDL exacto, tipos, `CHECK`s e índices.

### 5.1 Catálogo
- **libros**: id, titulo, autor(es), editorial, categoria_id, ubicacion, precio_venta, costo_promedio, ultimo_costo, stock_minimo, categoria_impositiva_id, origen_stock (`propio` | `consignacion`), estado (`nuevo`; campo previsto, **oculto en la UI**), activo.
- **codigos_libro**: id, libro_id, codigo, tipo (`ISBN13`, `ISBN10`, `EAN13`, `INTERNO`, `PROVEEDOR`), es_principal. `codigo` único. Búsqueda y escaneo consultan esta tabla.
- **categorias**: id, nombre, margen_objetivo (opcional).
- **editoriales** (opcional como tabla; puede ser texto normalizado). **[A COMPLETAR]** decidir.
- **proveedores**: id, nombre, cuit (opcional), contacto, condiciones_pago, es_consignatario, activo.
- **libro_proveedor** (opcional): proveedor habitual y código del proveedor.

### 5.2 Stock
- **movimientos_stock**: id, libro_id, fecha, tipo (`compra`, `venta`, `devolucion_cliente`, `devolucion_proveedor`, `ajuste`, `consignacion_recibida`, `consignacion_devuelta`, `conteo`, `inicial`), cantidad (con signo), costo_unitario, documento_tipo, documento_id, motivo, usuario_id, lote_importacion_id (para deshacer).
- **Stock físico** = suma de movimientos. **Stock disponible** = físico − reservado por encargos. Se puede mantener una columna/tabla de caché `stock_actual` actualizada en la misma transacción, con una verificación que la contraste contra los movimientos.

### 5.3 Compras (entradas)
- **compras**: id, proveedor_id, fecha, numero_factura, moneda, subtotal_neto, impuestos, total, estado_pago (`pendiente`, `parcial`, `pagada`), en_consignacion, notas.
- **compra_lineas**: compra_id, libro_id, cantidad, costo_unitario_neto, tasa_impuesto, monto_impuesto, total_linea.
- **pagos_proveedor**: id, compra_id o liquidacion_id, fecha, monto, medio_pago. (Cuentas a pagar.)

### 5.4 Ventas
- **ventas**: id, fecha_hora, cliente_id (nullable = consumidor final), medio_pago_id, moneda, subtotal_neto, descuento, recargo, impuestos, total, estado (`confirmada`, `anulada`), usuario_id, caja_id/turno_id, comprobante_id (nullable).
- **venta_lineas**: venta_id, libro_id, cantidad, precio_unitario_neto, descuento_linea, tasa_impuesto, monto_impuesto, total_linea, **costo_unitario_al_vender**, **ultimo_costo_al_vender**.
- **medios_pago**: id, nombre (`efectivo`, `transferencia`, `debito`, `credito`, `qr`), ajuste_porcentaje (recargo/descuento por defecto), activo.

### 5.5 Impuestos y facturación (estructuras previstas)
- **impuestos**: id, nombre (`Exento`, `General`, `Reducida`), tipo (`IVA`), tasa, vigente_desde, vigente_hasta, activo. Semilla: **Exento 0% activo**; General 21% y Reducida 10,5% **inactivos**.
- **categorias_impositivas** (o uso directo de `impuestos`): los libros apuntan a una; por defecto "Exento".
- **Líneas con impuestos múltiples**: tabla `linea_impuestos` (linea_tipo, linea_id, impuesto_id, base, tasa, monto) para permitir percepciones/retenciones futuras. Hoy se usa un único registro (IVA).
- **clientes**: id, nombre, tipo_documento (`CUIT`, `CUIL`, `DNI`), numero_documento, condicion_iva (`consumidor_final`, `monotributista`, `responsable_inscripto`, `exento`), domicilio, email, telefono. Opcional hoy.
- **comprobantes**: id, venta_id, tipo (`ticket_interno`, `factura_A`, `factura_B`, `factura_C`, `nota_credito`, ...), punto_venta, numero, fecha, estado, cliente_id, datos_fiscales (CAE, vencimiento CAE, XML/PDF) — vacíos hoy. Inmutable una vez emitido.
- **series_numeracion**: tipo, punto_venta, proximo_numero. Asignación sin saltos ni duplicados (dentro de transacción).
- **configuracion_negocio**: razón social, CUIT, condición ante IVA (monotributista / responsable inscripto / exento), domicilio, `precios_incluyen_impuesto` (bool), costo con/sin impuesto, moneda por defecto.

### 5.6 Operación comercial
- **devoluciones** y **devolucion_lineas**: tipo (`cliente`, `proveedor`), documento_origen_tipo/id, fecha, motivo, importes. Futuro: genera nota de crédito.
- **encargos**: id, cliente (o nombre libre), libro_id, cantidad, fecha, sena, estado (`pendiente`, `reservado`, `retirado`, `cancelado`).
- **consignacion_pendiente**: unidades vendidas de libros en consignación aún no liquidadas. **liquidaciones_consignacion** (+ detalle): cierre periódico que genera la cuenta a pagar. La deuda nace al vender, no al recibir.
- **gastos**: id, fecha, categoria_gasto_id, descripcion, monto, medio_pago, proveedor_id (opcional). **categorias_gasto**.
- **cajas / turnos**: apertura/cierre por usuario, con totales por medio de pago y diferencia declarada.
- **historial_precios**: libro_id, fecha, precio_venta_anterior/nuevo, costo, motivo (`manual`, `actualizacion_masiva`, `importacion`), usuario_id.

### 5.7 Sistema
- **usuarios**: id, nombre, rol_id, activo. Un único administrador, sesión automática.
- **roles** y **permisos** (rol↔acción). Roles: administrador, vendedor, consulta. Acciones sensibles: ver costos, ajustar stock, anular ventas, cambiar precios, importar, ver reportes financieros.
- **auditoria**: id, fecha, usuario_id, entidad, registro_id, campo, valor_anterior, valor_nuevo, motivo.
- **importaciones**: id, fecha, archivo, modo, resumen, estado (`aplicada`, `revertida`). Base del "deshacer".
- **mapeos_importacion**: nombre, mapeo_json (recordar el mapeo de columnas).
- **cache_metadatos_isbn**: isbn, titulo, autor, editorial, fuente, fecha.
- **schema_version / migraciones aplicadas**.
- **ajustes**: clave/valor (días de alerta de precio desactualizado, ventana de reposición, cantidad de backups a conservar, etc.).

---

## 6. Reglas de negocio clave

### 6.1 Costos
- **Costo promedio ponderado** recalculado en cada compra: `(stock_actual × costo_actual + cant × costo_nuevo) / (stock_actual + cant)`.
- Se guarda también el **último costo de compra** (costo de reposición).
- Cada venta congela `costo_unitario_al_vender` y `ultimo_costo_al_vender`.

### 6.2 Ventas
- Confirmar una venta: valida stock disponible (con opción configurable de permitir stock negativo con aviso), crea líneas, movimientos de stock, ajusta caja, emite ticket interno, todo en una transacción.
- Anular una venta: genera movimientos inversos; no borra.
- Precio de lista vs. medio de pago: el medio puede aplicar recargo o descuento (p. ej. precio efectivo).

### 6.3 Compras y consignación
- Compra normal: aumenta stock, recalcula costos, genera cuenta a pagar si no está pagada.
- Consignación: ingresa stock **sin deuda**. Al vender, se registra unidad pendiente de liquidar. La liquidación periódica cierra esas unidades y genera la cuenta a pagar.

### 6.4 Precios e inflación
- **Actualización masiva de precios** por porcentaje o monto, por selección, categoría, editorial o proveedor; **vista previa** (antes/después, margen resultante), redondeo configurable (p. ej. a múltiplos de $10 o $50), historial y posibilidad de revertir.
- **Precio sugerido** = último costo × (1 + margen objetivo), con margen por categoría/editorial.
- **Aviso de precios desactualizados**: libros sin cambio de precio hace más de X días.
- Reporte de margen con dos columnas: sobre **costo histórico** y sobre **último costo**.

### 6.5 Impuestos
- Todo se calcula con impuestos aunque la tasa hoy sea 0%. Líneas guardan neto, tasa, monto de impuesto y total.
- Configuración: precios incluyen o no impuesto. Costo de mercadería con o sin IVA (si fuera crédito fiscal recuperable, sin IVA).
- Los reportes de resultado trabajan sobre **netos**. Reporte IVA ventas vs. IVA compras (hoy en cero).
- Previsto: más de un impuesto por línea (percepciones, Ingresos Brutos).

### 6.6 Facturación (futuro)
- La **venta** es independiente del **comprobante**. Hoy solo existe el emisor **"ticket interno"**, PDF simple con leyenda explícita **"Comprobante no válido como factura"**.
- Interfaz común `Emisor` con una implementación hoy; un emisor ARCA (ex AFIP) se agregará después sin tocar la pantalla de venta.
- Previsto: tipo de comprobante según condición del titular (Factura C para monotributo; A/B para responsable inscripto), validación de CUIT/CUIL/DNI con dígito verificador, condición del cliente ante IVA.

### 6.7 Códigos
- **ISBN**: validar ISBN-13 e ISBN-10 (dígito verificador; conversión 10→13). Aceptar con o sin guiones. Tolerar prefijo 978-987.
- **Libros sin ISBN**: código interno generado por el sistema, con prefijo reservado, imprimible como etiqueta.
- Un libro puede tener varios códigos; el escaneo busca en `codigos_libro`.

### 6.8 Contabilidad básica (estado de resultados simple)
- Ingresos (ventas netas) − Costo de mercadería vendida = **Margen bruto**.
- Margen bruto − Gastos = **Resultado**.
- Valor de inventario: a costo promedio, a último costo y a precio de venta.
- Cuentas a pagar (compras y liquidaciones pendientes).
- Cierre de caja diario por medio de pago, por usuario y turno.
- No es contabilidad de doble entrada.

### 6.9 Reposición
- Sobre ventas de los últimos N días (configurable), rotación, stock mínimo y cobertura deseada. Resultado: lista por proveedor, cantidades editables, exportable como pedido (Excel/PDF).

### 6.10 Conteo físico
- Modo inventario: se escanea cada libro, el sistema compara contra el stock y propone ajustes (movimientos tipo `conteo`), confirmables uno a uno o en bloque.

---

## 7. Pantallas

1. **Inicio**: ventas del día y del mes, libros bajo mínimo, precios desactualizados, aviso de backup antiguo, últimos movimientos.
2. **Libros**: tabla con búsqueda instantánea (título, autor, ISBN, editorial), filtros (categoría, bajo mínimo, proveedor, activo), alta/edición/baja lógica, ficha con historial de movimientos y de precios.
3. **Venta (mostrador)**: campo de escaneo siempre enfocado (el lector actúa como teclado, termina con Enter), ticket en armado, medio de pago, descuento, confirmar/imprimir. Aviso sonoro/visual al leer; si el código no existe, ofrecer alta rápida.
4. **Compras**: proveedor, líneas, factura, pagada/pendiente, consignación.
5. **Proveedores, clientes (oculto/mínimo hoy), gastos**.
6. **Encargos y devoluciones**.
7. **Precios**: actualización masiva, sugeridos, desactualizados.
8. **Caja**: apertura, cierre, arqueo.
9. **Reportes**.
10. **Importación/Exportación**.
11. **Configuración**: negocio, impuestos, medios de pago, backups, ajustes.

Requisitos de UX: atajos de teclado en venta, navegación completa sin mouse en mostrador, formatos argentinos, mensajes de error claros en español. **[A COMPLETAR]** bocetos y flujos detallados.

---

## 8. Importación y exportación CSV

### 8.1 Plantilla oficial (descargable con fila de ejemplo, en `.csv` y `.xlsx`)

| Columna | Obligatoria | Notas |
|---|---|---|
| `isbn` | Sí* | ISBN-13/10, con o sin guiones |
| `titulo` | Sí | |
| `autor` | No | Varios separados por `;` |
| `editorial` | No | |
| `categoria` | No | Se crea si no existe |
| `precio_venta` | Sí | Acepta `12345,67` y `12345.67` |
| `costo` | No | Costo de compra unitario |
| `stock` | No | Cantidad inicial o a sumar |
| `stock_minimo` | No | |
| `ubicacion` | No | |
| `proveedor` | No | Se asocia si existe |
| `codigo_interno` | No | Para libros sin ISBN |

\* Sin ISBN, la fila requiere `codigo_interno` o se genera uno (el usuario decide en la vista previa).

### 8.2 Reglas
- Codificación UTF-8 (con o sin BOM) o la de Excel en Windows (cp1252); detección automática.
- Separador `,` o `;` detectado automáticamente (Excel argentino usa `;`).
- **ISBN siempre como texto.** Detectar notación científica (`9,78987E+12`) y avisar; ISBN con ceros o guiones preservados.
- Nombres de columna tolerantes (sin acentos, mayúsculas, sinónimos: `precio`, `pvp`, `precio de venta`, etc.).

### 8.3 Asistente en cuatro pasos
1. Elegir archivo.
2. Mapear columnas (recordar el mapeo).
3. **Vista previa con validación**: ISBN inválido, duplicados dentro del archivo y contra la base, precios vacíos o inválidos; filas problemáticas marcadas y excluibles.
4. Elegir el modo: **solo nuevos**, **actualizar existentes** o **sumar al stock**. Resumen final y botón **deshacer** que revierte toda la importación (usa `importaciones` y `lote_importacion_id`).

### 8.4 Exportación
Mismo formato que la plantilla, para sacar el catálogo, editarlo y reimportarlo.

---

## 9. Reportes (exportables a Excel y PDF)

- Stock actual; libros bajo mínimo.
- Ventas por día, mes, libro, autor, categoría, medio de pago.
- Más vendidos; **sin movimiento** hace X meses (capital dormido).
- Margen por libro y categoría (costo histórico y último costo).
- Compras por proveedor; cuentas a pagar.
- Resultado mensual (estado de resultados simple).
- Valor de inventario (costo, último costo, precio de venta).
- Cierre de caja.
- IVA ventas vs. compras (hoy en cero).
- Liquidaciones de consignación.
- Historial de precios.

Los reportes se calculan **en la base de datos** (SQL), no fila por fila en Python.

---

## 10. Copias de seguridad e integridad

- Copia automática al cerrar la app, conservando las últimas N (configurable).
- Copia manual desde configuración.
- Destino secundario configurable (pendrive, otra carpeta, carpeta sincronizada con la nube).
- Aviso al abrir si la última copia es antigua.
- `PRAGMA integrity_check` al iniciar; restauración guiada desde la app.
- Usar la API de backup de SQLite (copia consistente), no copiar el archivo en uso a ciegas.

---

## 11. Rendimiento y escala

- Pensada para cientos hoy, miles mañana; **probada con 5.000 y 20.000 libros sintéticos**.
- Índices en códigos, título, autor, editorial, categoría.
- Búsqueda instantánea con retardo (~200 ms) tras dejar de escribir; sin distinguir acentos ni mayúsculas ("garcia marquez" encuentra "García Márquez"). Previsto FTS5 más adelante.
- Listados cargados por demanda/paginados.
- Importación por lotes en una transacción.

---

## 12. Pruebas y calidad

- **pytest** sobre servicios y repositorios con base temporal: cálculo de costo promedio, ventas/anulaciones, stock derivado, importación (incluidos casos malos: ISBN científico, separadores, codificaciones), actualización de precios, impuestos con tasa 0% y con tasa 21% simulada, redondeos, consignación, backups, migraciones.
- Generador de **datos sintéticos** (`tools/`) para pruebas de volumen.
- Pruebas de interfaz mínimas en modo offscreen (la ventana abre, la búsqueda filtra).
- Registro de errores en `logs/` con mensajes comprensibles para el usuario.
- **[A COMPLETAR]** definir cobertura mínima y casos límite adicionales.

---

## 13. Fases de desarrollo

1. **Base**: esquema y migraciones, libros, códigos, CSV, búsqueda, stock, impuestos (Exento 0%), auditoría, copias de seguridad, usuario único y permisos "siempre sí".
2. **Operación**: proveedores, compras, ventas con ticket interno, devoluciones, caja, **actualización masiva de precios**.
3. **Administración**: gastos, resultado, inventario valorizado, cuentas a pagar, reportes y exportación.
4. **Comercial**: consignación, encargos, reposición, etiquetas, conteo físico con lector.
5. **Extensiones**: metadatos por ISBN, clientes, facturación ARCA, login y roles activos.

Cada fase termina con: pruebas pasando, app ejecutable, y un listado breve de cómo probarla a mano. Las estructuras de la fase 5 se crean desde la fase 1.

### Criterios de aceptación de la fase 1
- Crear, editar, desactivar y buscar libros; varios códigos por libro.
- Importar la plantilla oficial y un CSV "sucio" con vista previa, validación y deshacer.
- Stock derivado de movimientos, con ajustes motivados.
- Auditoría registrando cambios.
- Backup automático al cerrar y restauración.
- Migraciones funcionando.
- Búsqueda fluida con 20.000 libros sintéticos.
- Tests pasando.

---

## 14. Puntos a completar por quien implemente

1. DDL completo de SQLite con índices y restricciones.
2. Decidir si editoriales y autores son tablas o texto normalizado (autores múltiples).
3. Estrategia exacta de caché de stock vs. suma de movimientos.
4. Diseño detallado de pantallas y atajos de teclado.
5. Algoritmo de redondeo de precios y de sugerencia de reposición.
6. Fuente pública de metadatos por ISBN (fase 5) y manejo sin internet.
7. Formato exacto del ticket interno y de las etiquetas (tamaños de papel, rollos).
8. Script `build.bat` y pasos de empaquetado (incluyendo icono y recursos).
9. Textos de la interfaz (todo en español rioplatense neutro).
10. Cobertura de pruebas y casos límite.

## 15. Glosario

- **ARCA**: Agencia de Recaudación y Control Aduanero (ex AFIP).
- **CAE**: Código de Autorización Electrónico de un comprobante.
- **Consignación**: mercadería recibida que se paga solo al venderse.
- **Costo de reposición**: último costo de compra, lo que costaría reponer hoy.
- **Ticket interno**: comprobante no fiscal emitido por la app.
