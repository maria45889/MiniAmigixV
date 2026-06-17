---
title: "Duplicidad en navegación: botones y tarjetas duplicadas"
labels: ux, high-priority, design
---

## Descripción

Los accesos a secciones principales como "Música" o "Chat IA" aparecen duplicados: en el menú lateral y también como tarjetas grandes en el centro de la página, lo que puede confundir al usuario.

## Reproducción

1. Abrir la página de inicio.
2. Identificar enlaces a "Música" y "Chat IA" tanto en el sidebar como en las tarjetas centrales.

## Sugerencia

Mantener el sidebar como navegación global y convertir las tarjetas centrales en CTAs informativas (título corto + 1 línea de descripción) que dirijan a la misma ruta.

## Archivos sugeridos para editar

- `templates/index.html`
- `templates/includes/sidebar.html`
- `static/css/home.css`

## Pasos propuestos

1. Localizar enlaces duplicados en las plantillas.
2. Asegurar que las tarjetas centrales tengan descripciones cortas y un solo enlace objetivo.
3. Ajustar estilos para diferenciar claramente el sidebar (navegación) y las CTAs centrales.

## Criterios de aceptación

- Las CTAs centrales no duplican funciones del sidebar y poseen descripciones claras.
- Una prueba de clic confirma que llevan a la sección correcta.

## Prioridad

Alta
