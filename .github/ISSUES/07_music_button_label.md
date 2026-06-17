---
title: "Botón ambiguo 'Vincular a la matriz' — renombrar a acción clara"
labels: ux, high-priority, front-end
---

## Descripción

El botón con texto "Vincular a la matriz" es ambiguo y no comunica claramente la acción al usuario.

## Reproducción

1. Abrir la sección Música.
2. Localizar el botón con el texto "Vincular a la matriz".

## Sugerencia

Reemplazar por etiquetas descriptivas como `Añadir a la lista`, `Reproducir canción` o `Agregar a la cola`, según la acción real.

## Archivos sugeridos para editar

- `templates/music.html`
- `templates/includes/music_box.html`
- `static/js/music.js`

## Pasos propuestos

1. Confirmar la acción exacta del botón en el backend.
2. Elegir etiqueta descriptiva y actualizar plantillas.
3. Asegurar accesibilidad (`aria-label`).

## Prioridad

Alta
