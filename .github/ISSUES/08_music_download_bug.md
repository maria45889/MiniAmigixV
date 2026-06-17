---
title: "Descargas dañadas: 'Descarga exitosa' pero archivo inválido"
labels: bug, critical, backend
---

## Descripción

El sistema muestra una alerta de "Descarga exitosa", pero los archivos resultantes están dañados o no se pueden reproducir.

## Reproducción

1. Generar/descargar un archivo desde la sección Música.
2. Intentar reproducir o abrir el archivo descargado.

## Sugerencia

Revisar la lógica de empaquetado/streaming en el backend; añadir verificación (checksum, tamaño, mime-type) antes de marcar la descarga como exitosa.

## Archivos sugeridos para revisar

- `apps/music/views.py`
- `utils/downloads.py` (si existe)
- `static/js/download.js`

## Pasos propuestos

1. Reproducir el flujo de generación y descarga en desarrollo.
2. Añadir validaciones post-generación y manejo de errores.
3. Añadir tests automatizados que verifiquen integridad de los archivos.

## Prioridad

Critical
