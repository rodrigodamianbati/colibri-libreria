# Proyecto: Sistema de Gestión de Stock para Librería

## 1. Objetivo

Desarrollar una aplicación de escritorio para gestionar el inventario de una librería.

El sistema debe funcionar localmente en una notebook con Windows 10, sin requerir conexión a Internet ni servidores externos.

El desarrollo se realizará en otra computadora. Una vez terminado, se generará un instalador para el equipo del usuario final.

## 2. Stack tecnológico

| Componente | Tecnología | Estado |
|---|---|---|
| Aplicación de escritorio | Tauri 2 | Seleccionada |
| Frontend | React + TypeScript | Propuesta |
| Backend | Python | Seleccionada |
| Base de datos | SQLite | Seleccionada |
| Integración Python-Tauri | Sidecar | Propuesta |
| Sistema operativo de destino | Windows 10 | Confirmado |

### Frontend

Se propone utilizar React con TypeScript para desarrollar la interfaz gráfica.

El frontend será responsable de las pantallas, formularios, tablas, búsquedas, filtros y visualización de datos.

### Backend

El lenguaje seleccionado para el backend es **Python**, en lugar de desarrollar la lógica de negocio principalmente en Rust.

Python será responsable de las operaciones sobre productos, las validaciones, los movimientos de inventario y el acceso a SQLite.

Para integrarlo con Tauri 2 se utilizaría un proceso externo denominado *sidecar*, empaquetado junto con la aplicación.

Todavía debe decidirse cómo se comunicarán el frontend y Python:

- FastAPI mediante una API HTTP local.
- Comunicación entre procesos mediante entrada y salida estándar (stdin/stdout).

No se ha elegido definitivamente ninguna de estas dos alternativas.

### Base de datos

Se utilizará SQLite como base de datos local, sin necesidad de instalar un servidor de base de datos.

El archivo deberá almacenarse fuera del directorio de instalación para conservar la información al actualizar la aplicación.

Se contempla implementar mecanismos de copia de seguridad y restauración.

## 3. Arquitectura prevista

```text
Aplicación de escritorio
│
├── React + TypeScript
│   └── Interfaz de usuario
│
├── Tauri 2
│   └── Integración con Windows
│
├── Python (Sidecar)
│   ├── Lógica de negocio
│   ├── Validaciones
│   └── Persistencia
│
└── SQLite
    └── Base de datos local
```

## 4. Funcionalidades iniciales consideradas

El objetivo principal es gestionar el stock de productos de una librería.

Se han mencionado las siguientes funcionalidades como alcance inicial a definir:

- Gestión de productos.
- Gestión de categorías.
- Gestión de proveedores.
- Registro de entradas y salidas de stock.
- Consulta de existencias.
- Registro de ventas y actualización de stock.
- Copias de seguridad de la base de datos.

Estas funcionalidades todavía deben detallarse mediante requisitos y reglas de negocio.

## 5. Distribución e instalación

La aplicación debe poder instalarse en Windows 10 mediante un instalador generado por Tauri 2.

Se prefiere el formato `.exe` mediante NSIS.

El usuario final no deberá instalar herramientas de desarrollo como Python, Rust, Node.js o npm.

El backend Python deberá empaquetarse como ejecutable, por ejemplo utilizando PyInstaller, e incluirse como sidecar.

Tauri utilizará WebView2 para ejecutar el frontend. Será necesario comprobar su disponibilidad en el equipo de destino y resolver su instalación si falta.

La aplicación debe funcionar sin conexión a Internet durante su uso habitual.

## 6. Decisiones de arquitectura

- No utilizar un servidor de base de datos independiente.
- Mantener SQLite como almacenamiento local.
- Separar la interfaz de usuario de la lógica de negocio.
- Centralizar en Python las operaciones críticas que modifican el inventario.
- Utilizar transacciones para mantener la consistencia de los movimientos de stock.
- Conservar los datos del usuario independientemente de las actualizaciones del programa.
- Evitar dependencias de servicios externos para el funcionamiento principal.

## 7. Cuestiones pendientes

Antes de comenzar la implementación completa, deben resolverse:

1. Confirmar React + TypeScript como frontend definitivo.
2. Elegir el mecanismo de comunicación entre Tauri 2 y Python.
3. Definir los requisitos funcionales completos del sistema.
4. Diseñar el modelo de datos de SQLite.
5. Definir las reglas de negocio para entradas, salidas y ventas.
6. Confirmar la arquitectura de Windows (32 o 64 bits) y la versión exacta del equipo de destino.
7. Probar el empaquetado e instalación del backend Python como sidecar.
8. Diseñar el procedimiento de respaldo y restauración de datos.

## 8. Indicaciones para Codex

Utilizar este documento como contexto técnico inicial.

Respetar las tecnologías seleccionadas y distinguirlas de las alternativas todavía pendientes.

Antes de implementar nuevas funcionalidades:

1. Analizar los requisitos correspondientes.
2. Proponer la arquitectura o implementación.
3. Identificar las dependencias necesarias.
4. Evitar agregar frameworks o servicios que no estén justificados.
5. Priorizar la simplicidad, el mantenimiento y la compatibilidad con Windows 10.

**Estado actual del proyecto:** etapa de definición tecnológica y arquitectura. Todavía no se ha iniciado la implementación del sistema de inventario.