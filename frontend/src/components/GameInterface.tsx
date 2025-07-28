'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { useWebSocket } from '@/hooks/useWebSocket';
import { GamePlayRequest, GamePlayResponse, GameResult } from '@/types';
import GameHistory from './GameHistory';
import UserStats from './UserStats';

export default function GameInterface() {
  const [number, setNumber] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<GamePlayResponse[]>([]);
  const [error, setError] = useState<string>('');
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [activePanel, setActivePanel] = useState<'results' | 'history' | 'stats'>('results');
  const router = useRouter();

  // Check authentication on component mount
  useEffect(() => {
            const checkAuth = async () => {
          try {
            const auth = await apiClient.checkAuth();
            setIsAuthenticated(auth);
            if (!auth) {
              router.push('/login');
            }
          } catch (err) {
            setIsAuthenticated(false);
            router.push('/login');
          }
        };
    
    checkAuth();
  }, [router]);

  const { isConnected } = useWebSocket({
    onGameResult: (result) => {
      setResults(prev => [result, ...prev.slice(0, 9)]); // Keep last 10 results
    },
            onConnectionChange: (connected) => {
          // Connection status is handled by the UI
        },
    enabled: isAuthenticated === true, // Only connect if authenticated
  });

  // Log when authentication state changes
  

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const num = parseInt(number);
    
    if (!num || num < 1 || num > 9999) {
      setError('Please enter a valid number between 1 and 9999');
      return;
    }

    setError('');
    setIsLoading(true);

    try {
      const request: GamePlayRequest = { number: num };
      await apiClient.playGame(request);
      setNumber('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to play game');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await apiClient.logout();
      router.push('/login');
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  // Show loading while checking authentication
  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  // Redirect if not authenticated
  if (isAuthenticated === false) {
    return null; // Router will handle redirect
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600 p-4">
      {/* Connection Status */}
      <div className="fixed top-4 right-4 z-50">
        <div className={`px-4 py-2 rounded-full text-white font-semibold text-sm ${
          isConnected ? 'bg-green-500' : 'bg-red-500'
        }`}>
          {isConnected ? 'Connected' : 'Disconnected'}
        </div>
      </div>

      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex justify-between items-center">
          <h1 className="text-4xl font-bold text-white">🎲 NumberPlay</h1>
          <button
            onClick={handleLogout}
            className="bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Logout
          </button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Game Panel */}
        <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">
            🎮 Play Game
          </h2>
          
          <p className="text-center text-gray-600 mb-8">
            Enter a number and see if you win! Even numbers win, odd numbers lose.
          </p>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="number" className="block text-sm font-medium text-gray-900 mb-2">
                Enter your number (1-9999)
              </label>
              <input
                type="number"
                id="number"
                value={number}
                onChange={(e) => setNumber(e.target.value)}
                min="1"
                max="9999"
                required
                className="w-full px-6 py-4 text-2xl text-center border-3 border-gray-300 text-black rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Enter number..."
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !isConnected}
              className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold py-4 px-8 rounded-xl hover:from-purple-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 text-lg"
            >
              {isLoading ? '⏳ Processing...' : '🎮 Play Game'}
            </button>
          </form>

          {/* Prize Rules */}
          <div className="mt-8 p-6 bg-gray-50 rounded-xl">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">🎯 Prize Rules:</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• Numbers &gt; 900: 70% of number</li>
              <li>• Numbers &gt; 600: 50% of number</li>
              <li>• Numbers &gt; 300: 30% of number</li>
              <li>• Numbers ≤ 300: 10% of number</li>
            </ul>
          </div>
        </div>

        {/* Right Panel with Tabs */}
        <div className="space-y-4">
          {/* Tab Navigation */}
          <div className="flex space-x-2 bg-white/95 backdrop-blur-sm rounded-2xl p-2 shadow-2xl">
            <button
              onClick={() => setActivePanel('results')}
              className={`flex-1 py-2 px-4 rounded-xl font-medium transition-colors ${
                activePanel === 'results'
                  ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              📊 Live Results
            </button>
            <button
              onClick={() => setActivePanel('history')}
              className={`flex-1 py-2 px-4 rounded-xl font-medium transition-colors ${
                activePanel === 'history'
                  ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              📚 History
            </button>
            <button
              onClick={() => setActivePanel('stats')}
              className={`flex-1 py-2 px-4 rounded-xl font-medium transition-colors ${
                activePanel === 'stats'
                  ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              📈 Stats
            </button>
          </div>

          {/* Tab Content */}
          {activePanel === 'results' && (
            <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
              <h3 className="text-2xl font-bold text-center text-gray-800 mb-6">
                📊 Live Results
              </h3>
              
              <div className="max-h-96 overflow-y-auto space-y-4">
                {results.length === 0 ? (
                  <p className="text-center text-gray-500 py-8">
                    Your game results will appear here...
                  </p>
                ) : (
                  results.map((result, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-xl text-white ${
                        result.result === 'win'
                          ? 'bg-gradient-to-r from-green-500 to-emerald-500'
                          : 'bg-gradient-to-r from-red-500 to-orange-500'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="text-lg font-semibold">
                            {result.result === 'win' ? '🎉 WIN!' : '😔 LOSE'}
                          </h4>
                          <p className="text-sm opacity-90">
                            Number: <strong>{result.number}</strong>
                          </p>
                          {result.result === 'win' && result.prize && (
                            <p className="text-sm opacity-90">
                              Prize: <strong>${result.prize}</strong>
                            </p>
                          )}
                        </div>
                        <div className="text-xs opacity-75">
                          {new Date().toLocaleTimeString()}
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {activePanel === 'history' && <GameHistory />}
          {activePanel === 'stats' && <UserStats />}
        </div>
      </div>
    </div>
  );
} 