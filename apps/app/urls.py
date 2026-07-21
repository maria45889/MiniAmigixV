from django.urls import path, include

from . import views



urlpatterns = [

    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),

    path('register/', views.register_view, name='register'),

    path('chat/', views.chat_view, name='chat'),

    path('api/chat/', views.chat_api, name='chat_api'),

    path('musica/', views.musica, name='musica'),

    path('api/add-song/', views.add_song_api, name='add_song_api'),

    path('api/stream-audio/<str:youtube_id>/', views.stream_audio_api, name='stream_audio_api'),

    path('api/get-audio-stream/', views.get_audio_stream_api, name='get_audio_stream_api'),

    path('api/update-theme/', views.update_theme_api, name='update_theme_api'),

    path('api/update-language/', views.update_language_api, name='update_language_api'),

    path('api/search-lyrics/', views.search_lyrics_api, name='search_lyrics_api'),

    path('api/get-lyrics/<int:song_id>/', views.get_lyrics_api, name='get_lyrics_api'),

    path('api/save-lyrics/<int:song_id>/', views.save_lyrics_api, name='save_lyrics_api'),

    path('api/netease-lyrics/', views.netease_lyrics_api, name='netease_lyrics_api'),

    path('api/download-media/', views.download_media_api, name='download_media_api'),

    path('api/delete-chat/<int:chat_id>/', views.delete_chat_api, name='delete_chat_api'),

    path('api/delete-song/<int:song_id>/', views.delete_song_api, name='delete_song_api'),

    path('api/edit-song/<int:song_id>/', views.edit_song_api, name='edit_song_api'),

    path('api/crear-playlist/', views.crear_playlist, name='crear_playlist'),

    path('api/agregar-a-playlist/', views.agregar_a_playlist, name='agregar_a_playlist'),

    path('api/toggle-favorito/', views.toggle_favorito, name='toggle_favorito'),

    path('juegos/', views.juegos, name='juegos'),

    path('api/guardar-puntuacion/', views.guardar_puntuacion, name='guardar_puntuacion'),

    path('traductor/', include('traductor.urls')),

    path('entretenimiento/', views.entretenimiento, name='entretenimiento'),

    path('logout/', views.logout_view, name='logout'),

    path('api/sugerencia-rapida/', views.enviar_sugerencia_rapida, name='sugerencia_rapida'),

    path('panel-admin/', views.panel_admin, name='panel_admin'),

    path('panel-admin/soporte/', views.admin_soporte, name='admin_soporte'),

    path('panel-admin/sugerencias/', views.admin_sugerencias, name='admin_sugerencias'),

    path('api/responder-ticket/<int:ticket_id>/', views.responder_ticket, name='responder_ticket'),

    path('api/responder-sugerencia/<int:sugerencia_id>/', views.responder_sugerencia, name='responder_sugerencia'),

    path('panel-admin/user-email/<int:user_id>/', views.panel_admin_email_user, name='panel_admin_email_user'),

    path('api/admin/stats/', views.admin_stats_api, name='admin_stats_api'),

    path('panel-admin/exportar-excel/', views.exportar_reporte_excel, name='exportar_reporte_excel'),

    path('estudio/', include('estudio.urls')),

    path('eventos/', include('eventos.urls')),

    path('ir/eventos/', views.eventos, name='eventos'),

    path('soporte/', include('soporte.urls')),

    path('configuracion/', include('configuracion.urls')),

    path('perfil/', include('perfil.urls')),

    path('notificaciones/', include('notificaciones.urls')),

    path('sugerencias/', include('sugerencias.urls')),

    path('tutorial/', include('tutorial.urls')),

]

