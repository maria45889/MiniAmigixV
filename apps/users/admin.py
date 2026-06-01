from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.utils.html import format_html
from .models import Sugerencia, SupportTicket, Profile, Notification

def enviar_respuesta_sugerencia(sugerencia):
    """Envía notificación por email cuando se responde a una sugerencia"""
    if not sugerencia.respuesta:
        return  # No hay respuesta que notificar
    
    now = timezone.localtime(timezone.now())
    autor_nombre = sugerencia.user.get_full_name() or sugerencia.user.username
    autor_email = sugerencia.user.email or '(sin email)'
    
    subject = f"[MiniAmigixV] Respuesta a tu sugerencia: {sugerencia.titulo}"
    
    context = {
        'autor_nombre': autor_nombre,
        'autor_email': autor_email,
        'sugerencia_titulo': sugerencia.titulo,
        'tipo_display': sugerencia.get_tipo_display(),
        'tipo_clase': sugerencia.tipo.lower(),
        'estado_original_display': sugerencia.get_estado_display(),
        'estado_original_clase': sugerencia.estado.lower(),
        'fecha_envio': sugerencia.created_at.strftime('%d/%m/%Y %H:%M'),
        'respuesta': sugerencia.respuesta,
        'respondido_por': sugerencia.respondido_por.get_full_name() or sugerencia.respondido_por.username if sugerencia.respondido_por else 'Equipo',
        'fecha_respuesta': now.strftime('%d/%m/%Y %H:%M'),
        'estado_actual_display': sugerencia.get_estado_display(),
        'estado_actual_clase': sugerencia.estado.lower(),
        'sugerencia_id': sugerencia.id,
        'año': now.year,
    }

    try:
        html_content = render_to_string('emails/respuesta_sugerencia.html', context)
        
        msg = EmailMultiAlternatives(
            subject,
            '',  # Versión de texto plano (vacía, solo usamos HTML)
            settings.DEFAULT_FROM_EMAIL,
            [sugerencia.user.email] if sugerencia.user.email else []
        )
        if sugerencia.user.email:
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    except Exception:
        # Fallback silencioso para no romper el admin si falla el email
        pass

@admin.register(Sugerencia)
class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'usuario_nombre', 'usuario_email', 'tipo_colored', 'estado_colored', 'created_at')
    list_filter = ('tipo', 'estado', 'created_at')
    search_fields = ('titulo', 'descripcion', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    actions = ['marcar_como_resuelta', 'marcar_como_en_revision', 'marcar_como_pendiente']
    
    def usuario_nombre(self, obj):
        return obj.user.get_full_name() or obj.user.username
    usuario_nombre.short_description = 'Usuario'
    usuario_nombre.admin_order_field = 'user__first_name'
    
    def usuario_email(self, obj):
        return obj.user.email or '(sin email)'
    usuario_email.short_description = 'Email'
    usuario_email.admin_order_field = 'user__email'
    
    def tipo_colored(self, obj):
        color_map = {
            'idea': '#28a745',      # green
            'mejora': '#17a2b8',    # blue
            'reporte': '#dc3545',   # red
            'pregunta': '#ffc107',  # yellow
            'elogio': '#6f42c1',    # purple
            'otro': '#6c757d',      # gray
        }
        color = color_map.get(obj.tipo, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_tipo_display()
        )
    tipo_colored.short_description = 'Tipo'
    
    def estado_colored(self, obj):
        color_map = {
            'pendiente': '#ffc107',   # yellow
            'en_revision': '#17a2b8', # blue
            'respuesta': '#6f42c1',   # purple
            'resuelta': '#28a745',    # green
        }
        color = color_map.get(obj.estado, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_colored.short_description = 'Estado'
    
    def marcar_como_resuelta(self, request, queryset):
        updated = queryset.update(estado='respuesta', respondido_por=request.user, respondido_en=timezone.now())
        self.message_user(request, f'{updated} sugerencias marcadas como respondidas.')
    marcar_como_resuelta.short_description = "Marcar selecciones como respondidas"
    
    def marcar_como_en_revision(self, request, queryset):
        updated = queryset.update(estado='en_revision')
        self.message_user(request, f'{updated} sugerencias marcadas como en revisión.')
    marcar_como_en_revision.short_description = "Marcar selecciones como en revisión"
    
    def marcar_como_pendiente(self, request, queryset):
        updated = queryset.update(estado='pendiente', respondido_por=None, respondido_en=None, respuesta='')
        self.message_user(request, f'{updated} sugerencias marcadas como pendientes.')
    marcar_como_pendiente.short_description = "Marcar selecciones como pendientes"
    
    def save_model(self, request, obj, form, change):
        # Detectar si se está agregando o modificando una respuesta
        if change:  # Si es una edición (no creación nueva)
            try:
                # Obtener el objeto original desde la base de datos
                original = Sugerencia.objects.get(pk=obj.pk)
                # Verificar si se agregó o modificó la respuesta
                if original.respuesta != obj.respuesta and obj.respuesta:
                    # Se agregó o actualizó una respuesta
                    obj.respondido_por = request.user
                    obj.respondido_en = timezone.now()
                    # Cambiar estado a respondida o resuelta según corresponda
                    if obj.estado == 'pendiente' or obj.estado == 'en_revision':
                        obj.estado = 'respuesta'
            except Sugerencia.DoesNotExist:
                pass  # Si ocurre algún error, continuar normalmente
        elif not change and obj.respuesta:
            # Si se crea nueva sugerencia con respuesta (inusual pero posible)
            obj.respondido_por = request.user
            obj.respondido_en = timezone.now()
            if obj.estado == 'pendiente':
                obj.estado = 'respuesta'
        
        # Guardar el objeto
        super().save_model(request, obj, form, change)
        
        # Enviar email de respuesta si corresponde (después de guardar)
        if change:  # Solo para actualizaciones
            try:
                original = Sugerencia.objects.get(pk=obj.pk)
                # Si la respuesta fue agregada/actualizada y el usuario tiene email
                if original.respuesta != obj.respuesta and obj.respuesta and obj.user.email:
                    enviar_respuesta_sugerencia(obj)
            except Sugerencia.DoesNotExist:
                pass

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'usuario_nombre', 'tipo_colored', 'prioridad_colored', 'estado_colored', 'created_at')
    list_filter = ('tipo', 'prioridad', 'estado', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    actions = ['marcar_como_resuelto', 'marcar_como_en_revision', 'marcar_como_abierto']
    
    def usuario_nombre(self, obj):
        return obj.user.get_full_name() or obj.user.username
    usuario_nombre.short_description = 'Usuario'
    usuario_nombre.admin_order_field = 'user__first_name'
    
    def tipo_colored(self, obj):
        color_map = {
            'ayuda': '#17a2b8',      # info blue
            'consulta': '#6f42c1',   # purple
            'sugerencia': '#fd7e14', # orange
            'problema': '#dc3545',   # red
            'solicitud': '#28a745',  # green
            'informacion': '#6c757d', # gray
        }
        color = color_map.get(obj.tipo, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_tipo_display()
        )
    tipo_colored.short_description = 'Tipo'
    
    def prioridad_colored(self, obj):
        color_map = {
            'baja': '#ffc107',   # yellow
            'media': '#fd7e14',  # orange
            'alta': '#dc3545',   # red
            'urgente': '#6f42c1', # purple
        }
        color = color_map.get(obj.prioridad, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_prioridad_display()
        )
    prioridad_colored.short_description = 'Prioridad'
    
    def estado_colored(self, obj):
        color_map = {
            'abierto': '#17a2b8',   # blue
            'en_revision': '#fd7e14', # orange
            'resuelto': '#28a745',   # green
        }
        color = color_map.get(obj.estado, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_colored.short_description = 'Estado'
    
    def marcar_como_resuelto(self, request, queryset):
        updated = queryset.update(estado='resuelto', respondido_por=request.user, respondido_en=timezone.now())
        self.message_user(request, f'{updated} tickets marcados como resueltos.')
    marcar_como_resuelto.short_description = "Marcar selecciones como resueltos"
    
    def marcar_como_en_revision(self, request, queryset):
        updated = queryset.update(estado='en_revision')
        self.message_user(request, f'{updated} tickets marcados como en revisión.')
    marcar_como_en_revision.short_description = "Marcar selecciones como en revisión"
    
    def marcar_como_abierto(self, request, queryset):
        updated = queryset.update(estado='abierto', respondido_por=None, respondido_en=None, respuesta='')
        self.message_user(request, f'{updated} tickets marcados como abiertos.')
    marcar_como_abierto.short_description = "Marcar selecciones como abiertos"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'ai_name', 'theme_preference')
    search_fields = ('user__username', 'display_name', 'ai_name')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read_colored', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    actions = ['marcar_como_leido', 'marcar_como_no_leido']
    
    def is_read_colored(self, obj):
        if obj.is_read:
            color = '#28a745'  # green
            text = 'Leído'
        else:
            color = '#ffc107'  # yellow
            text = 'No leído'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            text
        )
    is_read_colored.short_description = 'Estado de lectura'
    
    def marcar_como_leido(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notificaciones marcadas como leídas.')
    marcar_como_leido.short_description = "Marcar como leído"
    
    def marcar_como_no_leido(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notificaciones marcadas como no leídas.')
    marcar_como_no_leido.short_description = "Marcar como no leído"
