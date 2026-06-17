---
title: "Redundancia en la identidad de la marca en la página de inicio"
labels: ux, high-priority, design
---

## Descripción

El nombre/identidad del sitio aparece repetido en la barra superior, en el menú lateral izquierdo y en el contenido central de la página de inicio, lo que genera saturación visual.

## Reproducción

1. Abrir la página de inicio.
2. Observar el logo/nombre en el header, en el sidebar y en el centro de la página.

## Sugerencia

Mantener el logo/nombre sólo en la esquina superior izquierda (header) y usar el espacio central para un mensaje de bienvenida o breve descripción.

## Archivos sugeridos para editar

- `templates/base.html`
- `templates/index.html`
- `templates/includes/sidebar.html`

## Pasos propuestos

1. Buscar ocurrencias del nombre/logo en las plantillas.
2. Eliminar las réplicas en el contenido central y, si aplica, en el menú lateral.
3. Añadir un bloque de bienvenida en el centro (título + subtítulo, máximo 2 líneas).
4. Verificar en desktop y móvil.

## Criterios de aceptación

- El nombre aparece únicamente en el header superior.
- El contenido central muestra un mensaje de bienvenida corto.

## Prioridad

Alta
