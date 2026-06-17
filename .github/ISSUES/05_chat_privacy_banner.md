---
title: "Aviso de privacidad en chat ocupa demasiado espacio y no es cerrable"
labels: ux, medium-priority, accessibility
---

## Descripción

El aviso que indica que el historial no se guardará ocupa demasiado espacio y no ofrece una opción clara para cerrarlo.

## Reproducción

1. Abrir la sección Chat IA.
2. Observar el aviso de historial/privacidad.

## Sugerencia

Mostrar el aviso como un banner delgado o tarjeta dismissible con un botón "X" y persistir la preferencia del usuario.

## Archivos sugeridos para editar

- `templates/chat.html`
- `static/js/chat.js`
- `static/css/chat.css`

## Pasos propuestos

1. Implementar un banner dismissible con `role="status"`.
2. Guardar estado cerrado en `localStorage`.
3. Añadir pruebas de accesibilidad.

## Prioridad

Media
