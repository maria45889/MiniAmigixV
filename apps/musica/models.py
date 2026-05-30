from django.db import models


class Cancion(models.Model):
    """
    Stores a song entry with optional cached lyrics (plain & LRC synced).
    letra and synced_lyrics default to '' to avoid NoneType surprises in frontend.
    """
    titulo = models.CharField(max_length=300, db_index=True)
    artista = models.CharField(max_length=300, blank=True, default='', db_index=True)
    youtube_id = models.CharField(max_length=120, blank=True, default='')

    letra = models.TextField(blank=True, null=True, default='')
    synced_lyrics = models.TextField(blank=True, null=True, default='')

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Canción'
        verbose_name_plural = 'Canciones'
        ordering = ['-actualizado_en']
        indexes = [
            models.Index(fields=['titulo', 'artista']),
        ]

    def __str__(self):
        if self.artista:
            return f"{self.titulo} – {self.artista}"
        return self.titulo

    def tiene_letra(self):
        return bool(self.letra and self.letra.strip())
