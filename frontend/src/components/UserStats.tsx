'use client';

import { useState, useEffect } from 'react';
import { UserStatistics } from '@/types';
import { apiClient } from '@/lib/api';

export default function UserStats() {
  const [stats, setStats] = useState<UserStatistics | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const loadStats = async () => {
      try {
        setIsLoading(true);
        const data = await apiClient.getUserStatistics();
        setStats(data);
        setError('');
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load statistics');
      } finally {
        setIsLoading(false);
      }
    };

    loadStats();
  }, []);

  if (isLoading) {
    return (
      <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
        <h3 className="text-2xl font-bold text-center text-gray-800 mb-6">
          📊 Your Statistics
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
          📊 Your Statistics
        </h3>
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
        <h3 className="text-2xl font-bold text-center text-gray-800 mb-6">
          📊 Your Statistics
        </h3>
        <p className="text-center text-gray-500 py-8">
          No statistics available.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
      <h3 className="text-2xl font-bold text-center text-gray-800 mb-6">
        📊 Your Statistics
      </h3>
      
      <div className="grid grid-cols-2 gap-4">
        {/* Total Games */}
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 rounded-xl">
          <div className="text-2xl font-bold">{stats.total_games}</div>
          <div className="text-sm opacity-90">Total Games</div>
        </div>

        {/* Win Rate */}
        <div className="bg-gradient-to-r from-green-500 to-green-600 text-white p-4 rounded-xl">
          <div className="text-2xl font-bold">{stats.win_rate}%</div>
          <div className="text-sm opacity-90">Win Rate</div>
        </div>

        {/* Wins */}
        <div className="bg-gradient-to-r from-emerald-500 to-emerald-600 text-white p-4 rounded-xl">
          <div className="text-2xl font-bold">{stats.wins}</div>
          <div className="text-sm opacity-90">Wins</div>
        </div>

        {/* Losses */}
        <div className="bg-gradient-to-r from-red-500 to-red-600 text-white p-4 rounded-xl">
          <div className="text-2xl font-bold">{stats.losses}</div>
          <div className="text-sm opacity-90">Losses</div>
        </div>
      </div>

      {/* Prize Statistics */}
      <div className="mt-6 space-y-3">
        <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
          <span className="text-gray-700 font-medium">Total Prize:</span>
          <span className="text-green-600 font-bold">${stats.total_prize.toFixed(2)}</span>
        </div>
        
        <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
          <span className="text-gray-700 font-medium">Average Prize:</span>
          <span className="text-blue-600 font-bold">${stats.average_prize.toFixed(2)}</span>
        </div>
        
        <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
          <span className="text-gray-700 font-medium">Best Prize:</span>
          <span className="text-purple-600 font-bold">${stats.best_prize.toFixed(2)}</span>
        </div>
      </div>

      {/* Last Played */}
      {stats.last_played && (
        <div className="mt-4 p-3 bg-gray-50 rounded-lg">
          <div className="text-center">
            <span className="text-gray-700 font-medium">Last Played:</span>
            <div className="text-gray-600 text-sm mt-1">
              {new Date(stats.last_played).toLocaleString()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 