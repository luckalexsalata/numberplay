'use client';

import { useState, useEffect } from 'react';
import { GameResult } from '@/types';
import { apiClient } from '@/lib/api';

export default function GameHistory() {
  const [history, setHistory] = useState<GameResult[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const loadHistory = async () => {
      try {
        setIsLoading(true);
        const data = await apiClient.getGameHistory();
        setHistory(data);
        setError('');
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load game history');
      } finally {
        setIsLoading(false);
      }
    };

    loadHistory();
  }, []);

  if (isLoading) {
    return (
      <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
        <h3 className="text-2xl font-bold text-center text-gray-800 mb-6">
          📚 Game History
        </h3>
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
        <h3 className="text-2xl font-bold text-center text-gray-800 mb-6">
          📚 Game History
        </h3>
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
      <h3 className="text-2xl font-bold text-center text-gray-800 mb-6">
        📚 Game History
      </h3>
      
      <div className="max-h-96 overflow-y-auto space-y-4">
        {history.length === 0 ? (
          <p className="text-center text-gray-500 py-8">
            No games played yet. Start playing to see your history!
          </p>
        ) : (
          history.map((game) => (
            <div
              key={game.id}
              className={`p-4 rounded-xl text-white ${
                game.result === 'win'
                  ? 'bg-gradient-to-r from-green-500 to-emerald-500'
                  : 'bg-gradient-to-r from-red-500 to-orange-500'
              }`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-lg font-semibold">
                    {game.result === 'win' ? '🎉 WIN!' : '😔 LOSE'}
                  </h4>
                  <p className="text-sm opacity-90">
                    Number: <strong>{game.number}</strong>
                  </p>
                  {game.result === 'win' && game.formatted_prize && (
                    <p className="text-sm opacity-90">
                      Prize: <strong>{game.formatted_prize}</strong>
                    </p>
                  )}
                </div>
                <div className="text-xs opacity-75 text-right">
                  <div>{game.formatted_date}</div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
} 