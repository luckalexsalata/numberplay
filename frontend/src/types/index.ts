export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
}

export interface GameResult {
  id: number;
  user_username: string;
  number: number;
  result: 'win' | 'lose';
  prize?: number;
  formatted_prize?: string;
  formatted_date?: string;
  created_at: string;
}

export interface GamePlayRequest {
  number: number;
}

export interface GamePlayResponse {
  number: number;
  result: 'win' | 'lose';
  prize?: number;
}

export interface UserStatistics {
  total_games: number;
  wins: number;
  losses: number;
  win_rate: number;
  total_prize: number;
  average_prize: number;
  best_prize: number;
  last_played: string | null;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
}

export interface AuthResponse {
  message: string;
  user: User;
  access_token: string;
  refresh_token: string;
}

export interface WebSocketMessage {
  type: 'connection_established' | 'game_result' | 'pong' | 'error';
  message?: string;
  data?: GamePlayResponse;
} 