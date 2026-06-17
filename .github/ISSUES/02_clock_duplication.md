---
title: "Reloj duplicado en la interfaz (hora mostrada dos veces)"
labels: ux, medium-priority, bug
---

## Descripción

La hora actual se muestra en dos ubicaciones de la pantalla (por ejemplo, arriba del nombre principal y otra vez más abajo), lo que crea redundancia visual.

## Reproducción

1. Abrir la página de inicio.
2. Localizar las dos instancias del reloj.

## Sugerencia

Conservar sólo una instancia del reloj, preferiblemente en la esquina del header o en el pie de página.

## Archivos sugeridos para editar

- `templates/includes/header.html`
- `templates/includes/footer.html`
- `templates/index.html`

## Pasos propuestos

1. Buscar renders de la hora en plantillas y scripts JS.
2. Eliminar la instancia duplicada.
3. Verificar que la hora actualiza correctamente en la instancia retenida.

## Criterios de aceptación

- Solo existe una ubicación visible del reloj.
- La hora se actualiza correctamente y no aparece repetida al navegar.

## Prioridad

Media
