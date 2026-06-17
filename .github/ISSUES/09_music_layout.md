---
title: "Caja de canciones demasiado ancha y contenido alineado a la izquierda"
labels: ux, medium-priority, design
---

## Descripción

El contenedor para añadir canciones ocupa todo el ancho de la pantalla, pero su contenido está agrupado a la izquierda dejando un espacio vacío a la derecha.

## Reproducción

1. Abrir la sección Música en una pantalla ancha.
2. Observar la caja de añadir canciones y la distribución interna.

## Sugerencia

Limitar el ancho del contenedor (`max-width`) o centrar el contenido con `margin: 0 auto;` y ajustar paddings.

## Archivos sugeridos para editar

- `templates/includes/music_box.html`
- `static/css/music.css`

## Pasos propuestos

1. Ajustar CSS del contenedor (max-width, padding, centering).
2. Verificar responsividad y comportamiento en distintos anchos.

## Prioridad

Media
