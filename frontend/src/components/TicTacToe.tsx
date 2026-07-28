import React, { useState, useEffect } from 'react';
import './TicTacToe.css';

interface TicTacToeProps {
  onBack?: () => void;
}

const TicTacToe: React.FC<TicTacToeProps> = ({ onBack }) => {
  const [board, setBoard] = useState<string[]>(Array(9).fill(''));
  const [playerWins, setPlayerWins] = useState(0);
  const [aiWins, setAiWins] = useState(0);
  const [draws, setDraws] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState<string | null>(null);
  const [isPlayerTurn, setIsPlayerTurn] = useState(true);
  const [loading, setLoading] = useState(false);

  const handleCellClick = (index: number) => {
    if (board[index] !== '' || gameOver || !isPlayerTurn || loading) return;

    setLoading(true);
    
    // Call backend API
    fetch('/api/juegos/tictactoe/make_move/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        board: board,
        player_move: index,
      }),
    })
      .then(response => response.json())
      .then(data => {
        setBoard(data.board);
        setGameOver(data.game_over);
        setWinner(data.winner);
        setIsPlayerTurn(!data.game_over);
        
        if (data.game_over) {
          if (data.winner === 'X') {
            setPlayerWins(prev => prev + 1);
          } else if (data.winner === 'O') {
            setAiWins(prev => prev + 1);
          } else {
            setDraws(prev => prev + 1);
          }
        }
      })
      .catch(error => {
        console.error('Error making move:', error);
        // Fallback to local logic if API fails
        handleLocalMove(index);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const handleLocalMove = (index: number) => {
    const newBoard = [...board];
    newBoard[index] = 'X';
    
    const localWinner = checkWinner(newBoard);
    if (localWinner) {
      setBoard(newBoard);
      setGameOver(true);
      setWinner(localWinner);
      if (localWinner === 'X') {
        setPlayerWins(prev => prev + 1);
      }
      return;
    }
    
    if (!newBoard.includes('')) {
      setBoard(newBoard);
      setGameOver(true);
      setWinner('draw');
      setDraws(prev => prev + 1);
      return;
    }
    
    // Simple AI move
    const availableMoves = newBoard.map((cell, i) => cell === '' ? i : -1).filter(i => i !== -1);
    const aiMove = availableMoves[Math.floor(Math.random() * availableMoves.length)];
    newBoard[aiMove] = 'O';
    
    const aiWinner = checkWinner(newBoard);
    if (aiWinner) {
      setBoard(newBoard);
      setGameOver(true);
      setWinner(aiWinner);
      if (aiWinner === 'O') {
        setAiWins(prev => prev + 1);
      }
      return;
    }
    
    if (!newBoard.includes('')) {
      setBoard(newBoard);
      setGameOver(true);
      setWinner('draw');
      setDraws(prev => prev + 1);
      return;
    }
    
    setBoard(newBoard);
  };

  const checkWinner = (board: string[]): string | null => {
    const winningCombinations = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8],
      [0, 3, 6], [1, 4, 7], [2, 5, 8],
      [0, 4, 8], [2, 4, 6]
    ];

    for (const combo of winningCombinations) {
      const [a, b, c] = combo;
      if (board[a] && board[a] === board[b] && board[a] === board[c]) {
        return board[a];
      }
    }
    return null;
  };

  const resetGame = () => {
    setBoard(Array(9).fill(''));
    setGameOver(false);
    setWinner(null);
    setIsPlayerTurn(true);
  };

  const getStatusMessage = () => {
    if (gameOver) {
      if (winner === 'X') return '¡Ganaste! 🎉';
      if (winner === 'O') return '¡Amigis ganó! 🤖';
      return '¡Empate! 🤝';
    }
    return '¡Juegas como ❌! Haz clic en una casilla para ganarme.';
  };

  return (
    <div className="tictactoe-container">
      {onBack && (
        <button className="back-button" onClick={onBack}>
          ← Volver
        </button>
      )}
      
      <div className="tictactoe-game">
        <h1 className="tictactoe-title">Tres en Raya ❌⭕</h1>
        
        <div className="tictactoe-host">
          <span className="host-label">Amigis Host</span>
        </div>
        
        <div className="tictactoe-status">
          {getStatusMessage()}
        </div>
        
        <div className="tictactoe-board">
          {board.map((cell, index) => (
            <button
              key={index}
              className={`tictactoe-cell ${cell ? 'filled' : ''} ${cell === 'X' ? 'player' : 'ai'}`}
              onClick={() => handleCellClick(index)}
              disabled={loading}
            >
              {cell}
            </button>
          ))}
        </div>
        
        <div className="tictactoe-scores">
          <div className="score-item">
            <span className="score-icon">❌</span>
            <span className="score-label">Tú:</span>
            <span className="score-value">{playerWins}</span>
          </div>
          <div className="score-item">
            <span className="score-icon">⭕</span>
            <span className="score-label">Amigis:</span>
            <span className="score-value">{aiWins}</span>
          </div>
          <div className="score-item">
            <span className="score-icon">🤝</span>
            <span className="score-label">Empates:</span>
            <span className="score-value">{draws}</span>
          </div>
        </div>
        
        <button 
          className="tictactoe-reset" 
          onClick={resetGame}
          disabled={loading}
        >
          Reiniciar Partido 🔄
        </button>
      </div>
    </div>
  );
};

export default TicTacToe;
