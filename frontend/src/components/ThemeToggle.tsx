import React from 'react';
import { useTheme } from '../contexts/ThemeContext';
import './ThemeToggle.css';

const ThemeToggle: React.FC = () => {
  try {
    const { theme, toggleTheme } = useTheme();
    return (
      <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
        {theme === 'dark' ? '🌙' : '☀️'}
      </button>
    );
  } catch (error) {
    // Fallback if ThemeProvider is not available
    return null;
  }
};

export default ThemeToggle;
