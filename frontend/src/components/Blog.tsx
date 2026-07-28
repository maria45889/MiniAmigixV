import React, { useState } from 'react';
import './Blog.css';

interface BlogPost {
  id: number;
  title: string;
  excerpt: string;
  category: string;
  author: string;
  date: string;
  readTime: string;
  image: string;
  featured?: boolean;
  likes?: number;
  comments?: number;
}

const Blog: React.FC = () => {
  const [activeCategory, setActiveCategory] = useState('Todo');
  const [searchQuery, setSearchQuery] = useState('');

  const categories = [
    { id: 'Todos', name: 'Todos', icon: '�' },
    { id: 'tecnologia', name: 'Tecnología', icon: '💻' },
    { id: 'ia', name: 'Inteligencia Artificial', icon: '🤖' },
    { id: 'educacion', name: 'Educación', icon: '📚' },
    { id: 'videojuegos', name: 'Videojuegos', icon: '�' },
    { id: 'musica', name: 'Música', icon: '�' },
    { id: 'idiomas', name: 'Idiomas', icon: '🌎' },
    { id: 'ciberseguridad', name: 'Ciberseguridad', icon: '🔒' },
    { id: 'aplicaciones', name: 'Aplicaciones', icon: '📱' },
  ];

  const featuredPosts: BlogPost[] = [
    {
      id: 1,
      title: '🚀 Novedades de MiniAmigixV 3.0: El Rediseño Total',
      excerpt: 'Conoce la nueva versión de MiniAmigixV con interfaz Glassmorphism, IA Chat mejorado con visión de imágenes y voz, reproductor musical inteligente, Sala Arcade de minijuegos y la Academia de Amigis.',
      category: 'tecnologia',
      author: 'Equipo MiniAmigixV',
      date: '24 de Julio, 2026',
      readTime: '4 min',
      image: '�',
      featured: true
    }
  ];

  const recentPosts: BlogPost[] = [
    {
      id: 2,
      title: '¿Qué es la IA Generativa y cómo funciona?',
      excerpt: 'Descubre los fundamentos detrás de los modelos GPT, redes neuronales y síntesis de contenido inteligente.',
      category: 'ia',
      author: 'Maria José',
      date: '23/7/2026',
      readTime: '3 min',
      image: '🤖',
      likes: 42,
      comments: 8
    },
    {
      id: 3,
      title: 'Cómo crear una API REST con Django y Python',
      excerpt: 'Aprende a estructurar tus endpoints, serializadores y autenticación en proyectos web backend.',
      category: 'tecnologia',
      author: 'Dev Team',
      date: '22/7/2026',
      readTime: '5 min',
      image: '💻',
      likes: 38,
      comments: 12
    },
    {
      id: 4,
      title: 'Tendencias de Diseño UI/UX para Interfaces Modernas',
      excerpt: 'Principios de cristal translúcido, gradientes dinámicos y experiencias de usuario memorables.',
      category: 'tecnologia',
      author: 'UX Studio',
      date: '21/7/2026',
      readTime: '4 min',
      image: '🎨',
      likes: 56,
      comments: 15
    },
    {
      id: 5,
      title: 'Consejos fundamentales de Ciberseguridad',
      excerpt: 'Protege tus cuentas personales, habilita 2FA y evita ataques de phishing con buenas prácticas.',
      category: 'ciberseguridad',
      author: 'Security Hub',
      date: '20/7/2026',
      readTime: '3 min',
      image: '🔒',
      likes: 29,
      comments: 5
    }
  ];

  const filteredPosts = recentPosts.filter(post => {
    const matchesCategory = activeCategory === 'Todo' || post.category === activeCategory;
    const matchesSearch = post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         post.excerpt.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const trendingTopics = [
    { id: 1, title: '¿Qué es la IA Generativa?', icon: '🤖' },
    { id: 2, title: 'API REST con Django', icon: '💻' },
    { id: 3, title: 'Tendencias UI/UX 2026', icon: '🎨' },
    { id: 4, title: 'Ciberseguridad Práctica', icon: '🔐' },
  ];

  const amigisRecommendations = [
    { id: 1, type: '💡 Truco de Código', content: 'Usa `list comprehension` en Python para crear listas de forma limpia.' },
    { id: 2, type: '📚 Dato Curioso', content: 'El primer "bug" informático fue una polilla real atrapada en una computadora en 1947.' },
    { id: 3, type: '🎵 Playlist Recom', content: 'Música lo-fi para estudiar' },
  ];

  const BlogCard: React.FC<{ post: BlogPost; featured?: boolean }> = ({ post, featured }) => (
    <div className={`blog-card ${featured ? 'featured' : ''}`}>
      <div className="blog-image">
        <span className="blog-icon">{post.image}</span>
        {featured && <span className="featured-badge">⭐ DESTACADO • NOVEDADES</span>}
      </div>
      <div className="blog-content">
        <div className="blog-meta">
          <span className="blog-category">{categories.find(c => c.id === post.category)?.icon} {categories.find(c => c.id === post.category)?.name}</span>
          <span className="blog-date">{post.date}</span>
        </div>
        <h3 className="blog-title">{post.title}</h3>
        <p className="blog-excerpt">{post.excerpt}</p>
        <div className="blog-footer">
          <span className="blog-author">👤 {post.author}</span>
          <span className="blog-read-time">⏱️ {post.readTime}</span>
        </div>
        {post.likes !== undefined && post.comments !== undefined && (
          <div className="blog-engagement">
            <span className="engagement-item">❤️ {post.likes}</span>
            <span className="engagement-item">💬 {post.comments}</span>
          </div>
        )}
        {featured && (
          <button className="read-more-btn">📖 Leer Artículo Completo</button>
        )}
      </div>
    </div>
  );

  return (
    <div className="blog-container">
      <div className="blog-header">
        <div className="header-title">
          <span className="header-icon">�</span>
          <div>
            <h1>Blog & Novedades</h1>
            <p>Descubre artículos, tutoriales, noticias tecnológicas y novedades de MiniAmigixV.</p>
          </div>
        </div>
      </div>

      {/* Search and Categories */}
      <div className="search-section">
        <div className="search-bar">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Buscar artículos..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="categories-header">
          <h3>Categorías</h3>
          <button className="create-article-btn">Crear Artículo</button>
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

      {/* Amigis Blog Section */}
      <div className="amigis-blog-section">
        <div className="amigis-blog-card">
          <div className="amigis-avatar">🦆</div>
          <div className="amigis-content">
            <h3>Amigis Blog</h3>
            <p>Blog de Amigis 🦆: "¡Hola! Hoy encontré un artículo fascinante que creo que te va a encantar. ¿Quieres leerlo? 📖"</p>
          </div>
        </div>
      </div>

      {/* Featured Posts */}
      {activeCategory === 'Todo' && !searchQuery && (
        <div className="featured-section">
          <div className="featured-grid">
            {featuredPosts.map((post) => (
              <BlogCard key={post.id} post={post} featured />
            ))}
          </div>
        </div>
      )}

      {/* Recent Posts */}
      <div className="posts-section">
        <div className="posts-grid">
          {filteredPosts.map((post) => (
            <BlogCard key={post.id} post={post} />
          ))}
        </div>
      </div>

      {/* Trending Topics */}
      {activeCategory === 'Todo' && !searchQuery && (
        <div className="trending-section">
          <div className="section-header">
            <h3>Temas en Tendencia</h3>
          </div>
          <div className="trending-list">
            {trendingTopics.map((topic, index) => (
              <div key={topic.id} className="trending-item">
                <span className="trending-rank">{index + 1}</span>
                <span className="trending-icon">{topic.icon}</span>
                <span className="trending-title">{topic.title}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Amigis Recommendations */}
      {activeCategory === 'Todo' && !searchQuery && (
        <div className="amigis-recommendations">
          <div className="section-header">
            <h3>Recomendados de Amigis</h3>
          </div>
          <div className="recommendations-list">
            {amigisRecommendations.map((rec) => (
              <div key={rec.id} className="recommendation-item">
                <span className="rec-type">{rec.type}</span>
                <p className="rec-content">{rec.content}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {filteredPosts.length === 0 && (
        <div className="empty-state">
          <span className="empty-icon">📭</span>
          <h3>No se encontraron artículos</h3>
          <p>Intenta con otra categoría o término de búsqueda.</p>
        </div>
      )}
    </div>
  );
};

export default Blog;
