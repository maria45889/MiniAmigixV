---
title: "Control de tema duplicado (modo claro/oscuro)"
labels: ux, high-priority, front-end
---

## Descripción

Existe un botón para cambiar el tema dentro del chat y otro botón general para toda la página, lo que genera confusión sobre el alcance del cambio.

## Reproducción

1. Localizar el switch de tema en la sección Chat IA y en la barra/menu principal.

## Sugerencia

Mantener un único control global (header o sidebar) que aplique el tema a toda la UI y persista la preferencia.

## Archivos sugeridos para editar

- `templates/includes/header.html`
- `templates/includes/sidebar.html`
- `static/js/theme.js`

## Pasos propuestos

1. Eliminar control secundario dentro del chat.
2. Asegurar persistencia en `localStorage`.
3. Verificar que el cambio afecte toda la UI.

## Prioridad

Alta
