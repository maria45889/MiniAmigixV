# TODO — MiniAmigixV (Bug JS + Admin seguro)

## Etapa A — Corregir `switchView()` y navegación (prioridad alta)
- [x] 1. Localizar en templates/ y JS dónde se usa `switchView()` (y verificar si existe o no en `main.js`).

- [x] 2. Corregir la implementación (exponer en `window` o reescribir usando `addEventListener` sin inline onclick).

- [ ] 3. Confirmar que el script que define `switchView()` carga (sin 404) y que no hay `type="module"` rompiendo el scope global.
- [ ] 4. Eliminar/o evitar listeners duplicados al cargar módulos por `fetch`.
- [ ] 5. Validar en consola/navegación que no vuelva a aparecer el error.

## Etapa B — Panel Administrativo “solo para ti” con seguridad real
- [x] 6. Identificar endpoints admin existentes (por ejemplo `/api/admin-stats/`, soporte admin, etc.).

- [x] 7. Implementar verificación de permisos estricta en backend (ideal: decorador `@admin_only` que valide `is_superuser`/`is_staff` y además usuario autorizado).
- [x] 8. Proteger views admin con `403 Forbidden` al fallar permisos.

- [x] 9. Proteger APIs admin con DRF permissions (y/o checks manuales).

- [ ] 10. Confirmar que el frontend o los botones no revelan controles admin a usuarios normales.
- [ ] 11. Confirmar que el acceso por URL a rutas admin responde 403/redirect seguro.


## Etapa C — UI / juegos / mejoras visuales
- [x] 12. Ocultar tiempo (preferencia + persiste + UI).

- [ ] 13. Unificar “idioma + notificaciones + modo” en una sola tuerca.


- [ ] 14. Arreglar modo claro (mezcla de colores).
- [ ] 15. Mejoras de Pop It contraste y animación.
- [ ] 16. Aumentar clicks en el juego.

