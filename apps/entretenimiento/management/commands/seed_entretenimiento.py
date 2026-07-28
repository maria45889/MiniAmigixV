from django.core.management.base import BaseCommand
from apps.entretenimiento.models import CategoriaEntretenimiento, ContenidoEntretenimiento


class Command(BaseCommand):
    help = 'Carga datos de ejemplo para el módulo de entretenimiento'

    def handle(self, *args, **options):
        self.stdout.write('Cargando datos de ejemplo para Entretenimiento...')
        
        # Crear categorías
        categorias_data = [
            {'nombre': 'Películas', 'icono': '🎬', 'orden': 1, 'descripcion': 'Las mejores películas de todos los tiempos'},
            {'nombre': 'Series', 'icono': '📺', 'orden': 2, 'descripcion': 'Series de TV y streaming'},
            {'nombre': 'Anime', 'icono': '🎌', 'orden': 3, 'descripcion': 'Anime japonés'},
            {'nombre': 'Libros', 'icono': '📚', 'orden': 4, 'descripcion': 'Libros recomendados'},
            {'nombre': 'Manga', 'icono': '📖', 'orden': 5, 'descripcion': 'Manga y cómics'},
            {'nombre': 'Música', 'icono': '🎵', 'orden': 6, 'descripcion': 'Álbumes y artistas'},
            {'nombre': 'Podcasts', 'icono': '🎙️', 'orden': 7, 'descripcion': 'Podcasts interesantes'},
            {'nombre': 'Documentales', 'icono': '🎥', 'orden': 8, 'descripcion': 'Documentales educativos'},
            {'nombre': 'Teatro', 'icono': '🎭', 'orden': 9, 'descripcion': 'Obras de teatro y musicales'},
        ]
        
        categorias = {}
        for cat_data in categorias_data:
            cat, created = CategoriaEntretenimiento.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={
                    'icono': cat_data['icono'],
                    'orden': cat_data['orden'],
                    'descripcion': cat_data['descripcion']
                }
            )
            categorias[cat.nombre] = cat
            if created:
                self.stdout.write(f'  ✓ Categoría creada: {cat.nombre}')
        
        # Crear contenido de ejemplo
        peliculas_data = [
            {
                'titulo': 'Inception',
                'tipo': 'pelicula',
                'genero': 'Ciencia Ficción',
                'descripcion': 'Un ladrón que roba secretos corporativos a través del uso de la tecnología de compartir sueños.',
                'imagen': 'https://image.tmdb.org/t/p/w500/9gk7admal4zl67YrxIo2AO08qX8.jpg',
                'trailer': 'https://www.youtube.com/watch?v=YoHD9XEInc0',
                'anio': 2010,
                'duracion': '148 min',
                'calificacion': 8.8,
                'director': 'Christopher Nolan',
                'plataforma': 'Netflix',
                'es_destacado': True,
            },
            {
                'titulo': 'The Dark Knight',
                'tipo': 'pelicula',
                'genero': 'Acción',
                'descripcion': 'Batman debe aceptar una de las mayores pruebas psicológicas y físicas de su capacidad para luchar contra la injusticia.',
                'imagen': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg',
                'trailer': 'https://www.youtube.com/watch?v=EXeTwQWrcwY',
                'anio': 2008,
                'duracion': '152 min',
                'calificacion': 9.0,
                'director': 'Christopher Nolan',
                'plataforma': 'HBO Max',
            },
            {
                'titulo': 'Interstellar',
                'tipo': 'pelicula',
                'genero': 'Ciencia Ficción',
                'descripcion': 'Un equipo de exploradores viaja a través de un agujero de gusano en el espacio en un intento de asegurar la supervivencia de la humanidad.',
                'imagen': 'https://image.tmdb.org/t/p/w500/gEU2QniL6C8zEfVfy23rUnLJpsp.jpg',
                'trailer': 'https://www.youtube.com/watch?v=zSWdZVtXT7E',
                'anio': 2014,
                'duracion': '169 min',
                'calificacion': 8.6,
                'director': 'Christopher Nolan',
                'plataforma': 'Paramount+',
            },
        ]
        
        series_data = [
            {
                'titulo': 'Breaking Bad',
                'tipo': 'serie',
                'genero': 'Drama',
                'descripcion': 'Un profesor de química de secundaria con cáncer terminal se asocia con un exalumno para fabricar y vender metanfetamina.',
                'imagen': 'https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg',
                'trailer': 'https://www.youtube.com/watch?v=HhesaQXLuRY',
                'anio': 2008,
                'duracion': '5 temporadas',
                'calificacion': 9.5,
                'director': 'Vince Gilligan',
                'plataforma': 'Netflix',
            },
            {
                'titulo': 'Stranger Things',
                'tipo': 'serie',
                'genero': 'Ciencia Ficción',
                'descripcion': 'Cuando un niño desaparece, sus amigos, la familia y la policía se ven envueltos en una serie de eventos misteriosos al tratar de encontrarlo.',
                'imagen': 'https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg',
                'trailer': 'https://www.youtube.com/watch?v=b9EkMc79ZSU',
                'anio': 2016,
                'duracion': '4 temporadas',
                'calificacion': 8.7,
                'director': 'Duffer Brothers',
                'plataforma': 'Netflix',
            },
        ]
        
        anime_data = [
            {
                'titulo': 'Attack on Titan',
                'tipo': 'anime',
                'genero': 'Acción',
                'descripcion': 'En un mundo donde la humanidad vive dentro de ciudades rodeadas por enormes muros que los protegen de los Titanes.',
                'imagen': 'https://image.tmdb.org/t/p/w500/x7KxQ6d8yWQrCqPEy7sR9VfJY.jpg',
                'trailer': 'https://www.youtube.com/watch?v=MGRFwU9E3y0',
                'anio': 2013,
                'duracion': '4 temporadas',
                'calificacion': 9.1,
                'director': 'Tetsuro Araki',
                'plataforma': 'Crunchyroll',
            },
            {
                'titulo': 'Demon Slayer',
                'tipo': 'anime',
                'genero': 'Acción',
                'descripcion': 'Un joven se convierte en demon slayer después de que su familia es masacrada y su hermana menor se convierte en un demonio.',
                'imagen': 'https://image.tmdb.org/t/p/w500/xUfRZu2mi8jH6SzQEYdB9am3cDE.jpg',
                'trailer': 'https://www.youtube.com/watch?v=S8_YVFLp6NQ',
                'anio': 2019,
                'duracion': '3 temporadas',
                'calificacion': 8.9,
                'director': 'Haruo Sotozaki',
                'plataforma': 'Crunchyroll',
            },
        ]
        
        libros_data = [
            {
                'titulo': '1984',
                'tipo': 'libro',
                'genero': 'Ciencia Ficción',
                'descripcion': 'Una novela distópica que presenta un futuro totalitario donde el gobierno controla todos los aspectos de la vida.',
                'imagen': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1348990566i/5470.jpg',
                'anio': 1949,
                'duracion': '328 páginas',
                'calificacion': 9.2,
                'director': 'George Orwell',
                'plataforma': 'Amazon Kindle',
            },
            {
                'titulo': 'El Principito',
                'tipo': 'libro',
                'genero': 'Ficción',
                'descripcion': 'Un joven príncipe explora varios planetas y aprende lecciones valiosas sobre la vida y el amor.',
                'imagen': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1579652334i/157993.jpg',
                'anio': 1943,
                'duracion': '96 páginas',
                'calificacion': 9.0,
                'director': 'Antoine de Saint-Exupéry',
                'plataforma': 'Amazon Kindle',
            },
        ]
        
        documentales_data = [
            {
                'titulo': 'Our Planet',
                'tipo': 'documental',
                'genero': 'Naturaleza',
                'descripcion': 'Una serie documental que explora la belleza natural de la Tierra y el impacto del cambio climático.',
                'imagen': 'https://image.tmdb.org/t/p/w500/vguVN5338rIKN1vw8BbMbJhCvI.jpg',
                'trailer': 'https://www.youtube.com/watch?v=SP6R8r1Iq8o',
                'anio': 2019,
                'duracion': '8 episodios',
                'calificacion': 9.0,
                'director': 'David Attenborough',
                'plataforma': 'Netflix',
            },
            {
                'titulo': 'The Social Dilemma',
                'tipo': 'documental',
                'genero': 'Tecnología',
                'descripcion': 'Expertos de tecnología llaman la atención sobre los peligros peligrosos de las redes sociales.',
                'imagen': 'https://image.tmdb.org/t/p/w500/7Xs0jWK9DmLqrKQNgClGW4s1WxZ.jpg',
                'trailer': 'https://www.youtube.com/watch?v=7mqR_e2seeM',
                'anio': 2020,
                'duracion': '94 min',
                'calificacion': 8.7,
                'director': 'Jeff Orlowski',
                'plataforma': 'Netflix',
            },
            {
                'titulo': 'Planet Earth',
                'tipo': 'documental',
                'genero': 'Naturaleza',
                'descripcion': 'Una serie documental que muestra la diversidad de la vida en la Tierra.',
                'imagen': 'https://image.tmdb.org/t/p/w500/9KqX5f8F6zT6r8r9r8r9r8r9r8r9r8r.jpg',
                'trailer': 'https://www.youtube.com/watch?v=JkaxUblCGz0',
                'anio': 2006,
                'duracion': '11 episodios',
                'calificacion': 9.4,
                'director': 'Alastair Fothergill',
                'plataforma': 'BBC',
            },
        ]
        
        teatro_data = [
            {
                'titulo': 'Hamilton',
                'tipo': 'teatro',
                'genero': 'Musical',
                'descripcion': 'Un musical que cuenta la historia de Alexander Hamilton, uno de los padres fundadores de los Estados Unidos.',
                'imagen': 'https://image.tmdb.org/t/p/w500/hZkgoQYus5vegHoetLkCJzb17zJ.jpg',
                'trailer': 'https://www.youtube.com/watch?v=SLsTbCkLkFg',
                'anio': 2015,
                'duracion': '2h 45min',
                'calificacion': 9.3,
                'director': 'Lin-Manuel Miranda',
                'plataforma': 'Disney+',
            },
            {
                'titulo': 'The Lion King',
                'tipo': 'teatro',
                'genero': 'Musical',
                'descripcion': 'La adaptación teatral del clásico de Disney sobre un león joven que debe asumir su destino como rey.',
                'imagen': 'https://image.tmdb.org/t/p/w500/tDl1J7sKq8sKq8sKq8sKq8sKq8sKq8s.jpg',
                'trailer': 'https://www.youtube.com/watch?v=4fMh0p9xX9g',
                'anio': 1997,
                'duracion': '2h 30min',
                'calificacion': 9.1,
                'director': 'Julie Taymor',
                'plataforma': 'Broadway',
            },
            {
                'titulo': 'Wicked',
                'tipo': 'teatro',
                'genero': 'Musical',
                'descripcion': 'La historia no contada de las brujas de Oz, antes de que Dorothy llegara.',
                'imagen': 'https://image.tmdb.org/t/p/w500/kq8sKq8sKq8sKq8sKq8sKq8sKq8sKq8.jpg',
                'trailer': 'https://www.youtube.com/watch?v=059s8sKq8sK',
                'anio': 2003,
                'duracion': '2h 45min',
                'calificacion': 8.9,
                'director': 'Joe Mantello',
                'plataforma': 'Broadway',
            },
        ]
        
        manga_data = [
            {
                'titulo': 'One Piece',
                'tipo': 'manga',
                'genero': 'Aventura',
                'descripcion': 'Monkey D. Luffy y su tripulación de piratas buscan el tesoro más grande del mundo, el One Piece.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/6/67/One_Piece_Volume_1_Cover.jpg',
                'anio': 1997,
                'duracion': '1000+ capítulos',
                'calificacion': 9.5,
                'director': 'Eiichiro Oda',
                'plataforma': 'MangaPlus',
            },
            {
                'titulo': 'Berserk',
                'tipo': 'manga',
                'genero': 'Fantasía Oscura',
                'descripcion': 'Guts, un mercenario solitario, viaja por un mundo medieval oscuro y brutal.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/4/4e/Berserk_volume_1.jpg',
                'anio': 1989,
                'duracion': '360+ capítulos',
                'calificacion': 9.4,
                'director': 'Kentaro Miura',
                'plataforma': 'Dark Horse',
            },
            {
                'titulo': 'My Hero Academia',
                'tipo': 'manga',
                'genero': 'Superhéroes',
                'descripcion': 'En un mundo donde la mayoría tiene superpoderes, Izuku Midoriya sueña con ser héroe.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/5/5e/My_Hero_Academia_volume_1_cover.jpg',
                'anio': 2014,
                'duracion': '400+ capítulos',
                'calificacion': 8.8,
                'director': 'Kohei Horikoshi',
                'plataforma': 'Viz Media',
            },
        ]
        
        musica_data = [
            {
                'titulo': 'Thriller',
                'tipo': 'musica',
                'genero': 'Pop',
                'descripcion': 'El álbum más vendido de todos los tiempos de Michael Jackson.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/5/50/Michael_Jackson_-_Thriller.png',
                'anio': 1982,
                'duracion': '42 min',
                'calificacion': 9.8,
                'director': 'Michael Jackson',
                'plataforma': 'Spotify',
            },
            {
                'titulo': 'Dark Side of the Moon',
                'tipo': 'musica',
                'genero': 'Rock Progresivo',
                'descripcion': 'El álbum icónico de Pink Floyd que explora temas de conflicto, greed y tiempo.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/3/3b/Dark_Side_of_the_Moon.png',
                'anio': 1973,
                'duracion': '43 min',
                'calificacion': 9.7,
                'director': 'Pink Floyd',
                'plataforma': 'Spotify',
            },
            {
                'titulo': 'Abbey Road',
                'tipo': 'musica',
                'genero': 'Rock',
                'descripcion': 'El undécimo álbum de estudio de The Beatles, considerado uno de los mejores álbumes de la historia.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/4/45/Abbey_Road_-_The_Beatles.jpg',
                'anio': 1969,
                'duracion': '47 min',
                'calificacion': 9.6,
                'director': 'The Beatles',
                'plataforma': 'Spotify',
            },
        ]
        
        podcast_data = [
            {
                'titulo': 'Serial',
                'tipo': 'podcast',
                'genero': 'True Crime',
                'descripcion': 'Un podcast investigativo que explora un caso de asesinato real no resuelto.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/3/3b/Serial_podcast_cover.jpg',
                'anio': 2014,
                'duracion': '12 episodios',
                'calificacion': 9.2,
                'director': 'Sarah Koenig',
                'plataforma': 'Spotify',
            },
            {
                'titulo': 'The Daily',
                'tipo': 'podcast',
                'genero': 'Noticias',
                'descripcion': 'El podcast de noticias diarias del New York Times.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/5/5e/The_Daily_podcast_cover.jpg',
                'anio': 2017,
                'duracion': '20-30 min por episodio',
                'calificacion': 8.9,
                'director': 'Michael Barbaro',
                'plataforma': 'Spotify',
            },
            {
                'titulo': 'Huberman Lab',
                'tipo': 'podcast',
                'genero': 'Ciencia',
                'descripcion': 'Un podcast sobre neurociencia y cómo optimizar el cerebro y el cuerpo.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/8/8e/Huberman_Lab_podcast_cover.jpg',
                'anio': 2021,
                'duracion': '1-2 horas por episodio',
                'calificacion': 9.4,
                'director': 'Andrew Huberman',
                'plataforma': 'Spotify',
            },
        ]
        
        # Combinar todos los datos
        all_content = peliculas_data + series_data + anime_data + libros_data + documentales_data + teatro_data + manga_data + musica_data + podcast_data
        
        for content_data in all_content:
            # Asignar categoría según tipo
            if content_data['tipo'] == 'pelicula':
                content_data['categoria'] = categorias['Películas']
            elif content_data['tipo'] == 'serie':
                content_data['categoria'] = categorias['Series']
            elif content_data['tipo'] == 'anime':
                content_data['categoria'] = categorias['Anime']
            elif content_data['tipo'] == 'libro':
                content_data['categoria'] = categorias['Libros']
            elif content_data['tipo'] == 'documental':
                content_data['categoria'] = categorias['Documentales']
            elif content_data['tipo'] == 'teatro':
                content_data['categoria'] = categorias['Teatro']
            elif content_data['tipo'] == 'manga':
                content_data['categoria'] = categorias['Manga']
            elif content_data['tipo'] == 'musica':
                content_data['categoria'] = categorias['Música']
            elif content_data['tipo'] == 'podcast':
                content_data['categoria'] = categorias['Podcasts']
            
            # Crear o actualizar contenido
            contenido, created = ContenidoEntretenimiento.objects.get_or_create(
                titulo=content_data['titulo'],
                tipo=content_data['tipo'],
                defaults=content_data
            )
            
            if created:
                self.stdout.write(f'  ✓ Contenido creado: {contenido.titulo} ({contenido.get_tipo_display()})')
            else:
                # Actualizar si ya existe
                for key, value in content_data.items():
                    setattr(contenido, key, value)
                contenido.save()
                self.stdout.write(f'  ✓ Contenido actualizado: {contenido.titulo}')
        
        self.stdout.write(self.style.SUCCESS('✓ Datos de ejemplo cargados exitosamente'))
