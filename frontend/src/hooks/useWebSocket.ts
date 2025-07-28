import { useEffect, useRef, useState, useCallback } from 'react';
import { WebSocketMessage, GamePlayResponse } from '@/types';

interface UseWebSocketOptions {
  onGameResult?: (result: GamePlayResponse) => void;
  onConnectionChange?: (connected: boolean) => void;
  enabled?: boolean; // Only connect if enabled (user is authenticated)
}

export function useWebSocket(options: UseWebSocketOptions = {}) {
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const optionsRef = useRef(options);
  optionsRef.current = options;

  const connect = useCallback(() => {
    if (!optionsRef.current.enabled) {
      return;
    }

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    // Get JWT token from localStorage
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('No authentication token found');
      return;
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.hostname}:8000/ws/game/?token=${token}`;
    
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      setError(null);
      optionsRef.current.onConnectionChange?.(true);
    };

    ws.onmessage = (event) => {
      try {
        const data: WebSocketMessage = JSON.parse(event.data);

        if (data.type === 'game_result' && data.data) {
          optionsRef.current.onGameResult?.(data.data);
        }
      } catch (err) {
        console.error('Error parsing WebSocket message:', err);
      }
    };

    ws.onclose = (event) => {
      setIsConnected(false);
      optionsRef.current.onConnectionChange?.(false);
      
      // Try to reconnect after 3 seconds
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      reconnectTimeoutRef.current = setTimeout(connect, 3000);
    };

    ws.onerror = (event) => {
      setError('WebSocket connection error');
      optionsRef.current.onConnectionChange?.(false);
    };
  }, []); // No dependencies since we use optionsRef

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  const sendPing = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'ping' }));
    }
  }, []);

  useEffect(() => {
    if (options.enabled) {
      // Add a small delay to ensure session is fully established
      const connectTimeout = setTimeout(() => {
        connect();
      }, 1000);

      // Keep connection alive with ping
      const pingInterval = setInterval(sendPing, 30000);

      return () => {
        clearTimeout(connectTimeout);
        clearInterval(pingInterval);
        disconnect();
      };
    } else {
      // If not enabled, disconnect any existing connection
      disconnect();
    }
  }, [options.enabled]); // Only depend on enabled state

  return {
    isConnected,
    error,
    connect,
    disconnect,
  };
} 