# SECURE_ADMIN_TODO

## Etapa B (Admin solo para mí) — Checklist
- [ ] 1) Definir el/los identificadores del admin autorizado (id/email) en `.env`.
- [ ] 2) Crear decorador `admin_only` (o `superuser_or_staff_and_allowed_user`) en backend.
- [ ] 3) Aplicar decorador a todas las vistas admin existentes (ej: `admin_support_view`).
- [ ] 4) Proteger endpoints API admin existentes (ej: `/api/admin-stats/`).
- [ ] 5) Asegurar respuesta `403 Forbidden` en backend.
- [ ] 6) En frontend: ocultar controles admin si backend no valida (defensa en profundidad).
- [ ] 7) Verificar que no exista acceso por URL a panel admin.

