---
title: "Títulos y migas de pan no reflejan la sección del Chat"
labels: ux, high-priority, front-end
---

## Descripción

Al entrar al chat, la barra superior sigue mostrando "Inicio" en lugar de "Chat IA", generando confusión sobre la ubicación del usuario.

## Reproducción

1. Navegar a la sección Chat IA.
2. Observar la barra superior y las migas de pan.

## Sugerencia

Hacer que el título de la página se actualice dinámicamente (pasando `page_title = "Chat IA"` desde la vista o usando bloques de plantilla).

## Archivos sugeridos para editar

- `templates/chat.html`
- `templates/includes/header.html`
- `apps/.../views.py` (vista del chat)

## Pasos propuestos

1. Añadir soporte de `page_title` en las plantillas base si no existe.
2. Actualizar la vista del chat para pasar el título adecuado.
3. Verificar en móvil y desktop.

## Prioridad

Alta
