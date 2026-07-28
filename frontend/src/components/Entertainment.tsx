import React, { useState } from 'react';
import './Entertainment.css';

interface ContentItem {
  id: number;
  title: string;
  rating?: number;
  year?: number;
  genre: string;
  author?: string;
  description?: string;
}

interface Category {
  id: string;
  name: string;
  icon: string;
}

const Entertainment: React.FC = () => {
  const [activeCategory, setActiveCategory] = useState('Todo');
  const [searchQuery, setSearchQuery] = useState('');
  const [aiRecommendation, setAiRecommendation] = useState<ContentItem | null>(null);

  const categories: Category[] = [
    { id: 'Todo', name: 'Todo', icon: '🔍' },
    { id: 'peliculas', name: 'Películas', icon: '🎬' },
    { id: 'series', name: 'Series', icon: '📺' },
    { id: 'anime', name: 'Anime', icon: '🎌' },
    { id: 'libros', name: 'Libros', icon: '📖' },
    { id: 'manga', name: 'Manga', icon: '📚' },
    { id: 'musica', name: 'Música', icon: '🎵' },
    { id: 'podcasts', name: 'Podcasts', icon: '🎙️' },
    { id: 'teatro', name: 'Teatro', icon: '🎭' },
    { id: 'documentales', name: 'Documentales', icon: '🎥' },
  ];

  const recommendationOfTheDay: ContentItem = {
    id: 1,
    title: 'Inception',
    rating: 8.8,
    year: 2010,
    genre: 'Ciencia Ficción',
    description: 'Un ladrón que roba secretos corporativos a través del uso de la tecnología de compartir sueños.'
  };

  const trending: ContentItem[] = [
    { id: 1, title: 'Breaking Bad', rating: 9.5, year: 2008, genre: 'Drama' },
    { id: 2, title: 'Attack on Titan', rating: 9.1, year: 2013, genre: 'Acción' },
    { id: 3, title: 'The Dark Knight', rating: 9.0, year: 2008, genre: 'Acción' },
  ];

  const popularMovies: ContentItem[] = [
    { id: 1, title: 'Inception', rating: 8.8, year: 2010, genre: 'Ciencia Ficción' },
    { id: 2, title: 'The Dark Knight', rating: 9.0, year: 2008, genre: 'Acción' },
    { id: 3, title: 'Interstellar', rating: 8.6, year: 2014, genre: 'Ciencia Ficción' },
  ];

  const featuredSeries: ContentItem[] = [
    { id: 1, title: 'Breaking Bad', rating: 9.5, year: 2008, genre: 'Drama' },
    { id: 2, title: 'Stranger Things', rating: 8.7, year: 2016, genre: 'Ciencia Ficción' },
  ];

  const topAnime: ContentItem[] = [
    { id: 1, title: 'Attack on Titan', rating: 9.1, year: 2013, genre: 'Acción' },
    { id: 2, title: 'Demon Slayer', rating: 8.9, year: 2019, genre: 'Acción' },
  ];

  const documentaries: ContentItem[] = [
    { id: 1, title: 'Planet Earth', rating: 9.4, year: 2006, genre: 'Naturaleza' },
    { id: 2, title: 'Our Planet', rating: 9.0, year: 2019, genre: 'Naturaleza' },
    { id: 3, title: 'The Social Dilemma', rating: 8.7, year: 2020, genre: 'Tecnología' },
  ];

  const recommendedBooks: ContentItem[] = [
    { id: 1, title: '1984', author: 'George Orwell' },
    { id: 2, title: 'El Principito', author: 'Antoine de Saint-Exupéry' },
  ];

  const theater: ContentItem[] = [
    { id: 1, title: 'Hamilton', author: 'Lin-Manuel Miranda' },
    { id: 2, title: 'The Lion King', author: 'Julie Taymor' },
    { id: 3, title: 'Wicked', author: 'Joe Mantello' },
  ];

  const popularManga: ContentItem[] = [
    { id: 1, title: 'One Piece', author: 'Eiichiro Oda' },
    { id: 2, title: 'Berserk', author: 'Kentaro Miura' },
    { id: 3, title: 'My Hero Academia', author: 'Kohei Horikoshi' },
  ];

  const featuredAlbums: ContentItem[] = [
    { id: 1, title: 'Thriller', rating: 9.8, year: 1982, genre: 'Michael Jackson' },
    { id: 2, title: 'Dark Side of the Moon', rating: 9.7, year: 1973, genre: 'Pink Floyd' },
    { id: 3, title: 'Abbey Road', rating: 9.6, year: 1969, genre: 'The Beatles' },
  ];

  const recommendedPodcasts: ContentItem[] = [
    { id: 1, title: 'Huberman Lab', rating: 9.4, year: 2021, genre: 'Andrew Huberman' },
    { id: 2, title: 'Serial', rating: 9.2, year: 2014, genre: 'Sarah Koenig' },
    { id: 3, title: 'The Daily', rating: 8.9, year: 2017, genre: 'Michael Barbaro' },
  ];

  const handleSurpriseMe = () => {
    const allContent = [
      ...popularMovies,
      ...featuredSeries,
      ...topAnime,
      ...documentaries,
      ...featuredAlbums,
      ...recommendedPodcasts
    ];
    const randomContent = allContent[Math.floor(Math.random() * allContent.length)];
    setAiRecommendation(randomContent);
  };

  const ContentCard: React.FC<{ item: ContentItem; type: 'movie' | 'series' | 'anime' | 'documentary' | 'album' | 'podcast' | 'book' | 'manga' | 'theater' }> = ({ item, type }) => (
    <div className="content-card">
      <div className="content-poster">
        <span className="content-icon">
          {type === 'movie' && '🎬'}
          {type === 'series' && '📺'}
          {type === 'anime' && '🎌'}
          {type === 'documentary' && '🎥'}
          {type === 'album' && '🎵'}
          {type === 'podcast' && '🎙️'}
          {type === 'book' && '📖'}
          {type === 'manga' && '📚'}
          {type === 'theater' && '🎭'}
        </span>
        <button className="favorite-btn">♡</button>
      </div>
      <div className="content-info">
        <h4>{item.title}</h4>
        {item.rating && <span className="rating">⭐ {item.rating}</span>}
        {item.year && <span className="year">{item.year}</span>}
        {item.author && <span className="author">{item.author}</span>}
        <p className="genre">{item.genre}</p>
      </div>
    </div>
  );

  return (
    <div className="entertainment-container">
      <div className="entertainment-header">
        <div className="header-title">
          <span className="header-icon">✨</span>
          <div>
            <h1>Entretenimiento</h1>
            <p>Descubre películas, series, libros y mucho más</p>
          </div>
        </div>
      </div>

      <div className="entertainment-description">
        <p>Explora nuestro catálogo curado con las mejores recomendaciones personalizadas para ti</p>
        <div className="stats">
          <div className="stat">
            <span className="stat-number">6</span>
            <span className="stat-label">Categorías</span>
          </div>
          <div className="stat">
            <span className="stat-number">100+</span>
            <span className="stat-label">Recomendaciones</span>
          </div>
          <div className="stat">
            <span className="stat-number">24/7</span>
            <span className="stat-label">Actualizado</span>
          </div>
        </div>
      </div>

      {/* Search and Categories */}
      <div className="search-section">
        <div className="search-bar">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Buscar película, serie o libro..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="categories">
          {categories.map((category) => (
            <button
              key={category.id}
              className={`category-btn ${activeCategory === category.id ? 'active' : ''}`}
              onClick={() => setActiveCategory(category.id)}
            >
              {category.icon} {category.name}
            </button>
          ))}
        </div>
      </div>

      {/* Recommendation of the Day */}
      <div className="recommendation-day">
        <div className="section-header">
          <h2>⭐ Recomendación del día</h2>
        </div>
        <div className="featured-card">
          <div className="featured-poster">
            <span className="featured-icon">🎬</span>
          </div>
          <div className="featured-info">
            <h3>{recommendationOfTheDay.title}</h3>
            <div className="featured-meta">
              <span className="rating">⭐ {recommendationOfTheDay.rating}/10</span>
              <span className="genre">{recommendationOfTheDay.genre}</span>
            </div>
            <p className="description">{recommendationOfTheDay.description}</p>
            <div className="featured-actions">
              <button className="action-btn primary">▶ Ver tráiler</button>
              <button className="action-btn secondary">♡ Añadir a favoritos</button>
            </div>
          </div>
        </div>
      </div>

      {/* AI Recommendation */}
      <div className="ai-recommendation">
        <div className="section-header">
          <h2>🤖 ¿Qué quieres ver hoy?</h2>
          <p>La IA te recomienda contenido basado en tus gustos</p>
        </div>
        <div className="ai-content">
          <button className="surprise-btn" onClick={handleSurpriseMe}>
            <span className="dice-icon">🎲</span>
            <span>Sorpréndeme</span>
          </button>
          <p className="ai-text">Deja que la IA elija algo para ti</p>
          {aiRecommendation && (
            <div className="ai-result">
              <h4>Te recomendamos: {aiRecommendation.title}</h4>
              {aiRecommendation.rating && <span>⭐ {aiRecommendation.rating}</span>}
              <p>{aiRecommendation.genre}</p>
            </div>
          )}
        </div>
      </div>

      {/* Trending */}
      <div className="content-section">
        <div className="section-header">
          <h2>🔥 Tendencias</h2>
        </div>
        <div className="trending-list">
          {trending.map((item, index) => (
            <div key={item.id} className="trending-item">
              <span className="rank">{index + 1}️⃣</span>
              <div className="trending-info">
                <h4>{item.title}</h4>
                <p>{item.genre}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Popular Movies */}
      <div className="content-section">
        <div className="section-header">
          <h2>Películas Populares</h2>
        </div>
        <div className="content-grid">
          {popularMovies.map((item) => (
            <ContentCard key={item.id} item={item} type="movie" />
          ))}
        </div>
      </div>

      {/* Featured Series */}
      <div className="content-section">
        <div className="section-header">
          <h2>Series Destacadas</h2>
        </div>
        <div className="content-grid">
          {featuredSeries.map((item) => (
            <ContentCard key={item.id} item={item} type="series" />
          ))}
        </div>
      </div>

      {/* Top Anime */}
      <div className="content-section">
        <div className="section-header">
          <h2>Top Anime</h2>
        </div>
        <div className="content-grid">
          {topAnime.map((item) => (
            <ContentCard key={item.id} item={item} type="anime" />
          ))}
        </div>
      </div>

      {/* Documentaries */}
      <div className="content-section">
        <div className="section-header">
          <h2>Documentales</h2>
        </div>
        <div className="content-grid">
          {documentaries.map((item) => (
            <ContentCard key={item.id} item={item} type="documentary" />
          ))}
        </div>
      </div>

      {/* Recommended Books */}
      <div className="content-section">
        <div className="section-header">
          <h2>Libros Recomendados</h2>
        </div>
        <div className="content-grid">
          {recommendedBooks.map((item) => (
            <ContentCard key={item.id} item={item} type="book" />
          ))}
        </div>
      </div>

      {/* Theater */}
      <div className="content-section">
        <div className="section-header">
          <h2>Obras de Teatro</h2>
        </div>
        <div className="content-grid">
          {theater.map((item) => (
            <ContentCard key={item.id} item={item} type="theater" />
          ))}
        </div>
      </div>

      {/* Popular Manga */}
      <div className="content-section">
        <div className="section-header">
          <h2>Manga Popular</h2>
        </div>
        <div className="content-grid">
          {popularManga.map((item) => (
            <ContentCard key={item.id} item={item} type="manga" />
          ))}
        </div>
      </div>

      {/* Featured Albums */}
      <div className="content-section">
        <div className="section-header">
          <h2>Álbumes Destacados</h2>
        </div>
        <div className="content-grid">
          {featuredAlbums.map((item) => (
            <ContentCard key={item.id} item={item} type="album" />
          ))}
        </div>
      </div>

      {/* Recommended Podcasts */}
      <div className="content-section">
        <div className="section-header">
          <h2>Podcasts Recomendados</h2>
        </div>
        <div className="content-grid">
          {recommendedPodcasts.map((item) => (
            <ContentCard key={item.id} item={item} type="podcast" />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Entertainment;
