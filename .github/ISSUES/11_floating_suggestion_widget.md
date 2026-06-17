---
title: "Widget de sugerencias flotante es intrusivo y se reposiciona"
labels: ux, high-priority, front-end
---

## Descripción

El botón/ventana flotante de sugerencias se reinicia y vuelve a su posición original al cambiar de pestaña, llegando a tapar contenido o resultar incómodo.

## Reproducción

1. Abrir la aplicación.
2. Mover o interactuar con el widget flotante.
3. Cambiar de pestaña; observar que el widget se reposiciona y puede tapar contenido.

## Sugerencia

Eliminar el widget flotante o reemplazarlo por un enlace fijo `Soporte`/`Contacto` en el sidebar o footer. Si se mantiene, hacer minimizable y persistente.

## Archivos sugeridos para editar

- `templates/includes/feedback_widget.html`
- `static/js/feedback_widget.js`
- `templates/includes/sidebar.html` o `templates/includes/footer.html`

## Pasos propuestos

1. Deshabilitar comportamiento reposicionador.
2. Añadir enlace fijo de soporte en sidebar/footer.
3. Probar en distintas resoluciones.

## Prioridad

High
