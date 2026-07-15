import React from 'react';

export const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-800">MiniAmigixV</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-2">💬 Chat IA</h2>
            <p className="text-gray-600">Conversa con MiniAmigix, tu asistente de IA</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-2">🎵 Música</h2>
            <p className="text-gray-600">Reproductor de música con YouTube</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-2">📅 Agenda</h2>
            <p className="text-gray-600">Calendario personal con recordatorios</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-2">🌤️ Clima</h2>
            <p className="text-gray-600">Información meteorológica en tiempo real</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-2">📚 Estudio</h2>
            <p className="text-gray-600">Recursos educativos organizados</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-2">🎭 Entretenimiento</h2>
            <p className="text-gray-600">Recomendaciones personalizadas</p>
          </div>
        </div>
      </main>
    </div>
  );
};
