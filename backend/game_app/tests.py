from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import GameResult
from .views import calculate_prize
import json

User = get_user_model()

class GameLogicTests(TestCase):
    """Test game logic and prize calculation"""
    
    def test_calculate_prize_over_900(self):
        """Test prize calculation for numbers > 900 (70%)"""
        self.assertEqual(calculate_prize(1000), 700.0)
        self.assertEqual(calculate_prize(950), 665.0)
        self.assertEqual(calculate_prize(9999), 6999.3)
    
    def test_calculate_prize_over_600(self):
        """Test prize calculation for numbers > 600 (50%)"""
        self.assertEqual(calculate_prize(800), 400.0)
        self.assertEqual(calculate_prize(700), 350.0)
        self.assertEqual(calculate_prize(900), 450.0)
    
    def test_calculate_prize_over_300(self):
        """Test prize calculation for numbers > 300 (30%)"""
        self.assertEqual(calculate_prize(500), 150.0)
        self.assertEqual(calculate_prize(400), 120.0)
        self.assertEqual(calculate_prize(600), 180.0)
    
    def test_calculate_prize_300_or_less(self):
        """Test prize calculation for numbers <= 300 (10%)"""
        self.assertEqual(calculate_prize(300), 30.0)
        self.assertEqual(calculate_prize(200), 20.0)
        self.assertEqual(calculate_prize(100), 10.0)
        self.assertEqual(calculate_prize(1), 0.1)
    
    def test_prize_rounding(self):
        """Test that prizes are properly rounded to 2 decimal places"""
        self.assertEqual(calculate_prize(333), 99.9)  # 333 * 0.3 = 99.9
        self.assertEqual(calculate_prize(777), 388.5)  # 777 * 0.5 = 388.5


class GameAPITests(APITestCase):
    """Test game API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_play_game_win_even_number(self):
        """Test playing game with even number (win)"""
        data = {'number': 842}
        response = self.client.post('/api/game/play/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number'], 842)
        self.assertEqual(response.data['result'], 'win')
        self.assertEqual(response.data['prize'], 421.0)  # 842 * 0.5 = 421.0
        
        # Check database record
        game_result = GameResult.objects.first()
        self.assertEqual(game_result.user, self.user)
        self.assertEqual(game_result.number, 842)
        self.assertEqual(game_result.result, 'win')
        self.assertEqual(float(game_result.prize), 421.0)
    
    def test_play_game_lose_odd_number(self):
        """Test playing game with odd number (lose)"""
        data = {'number': 841}
        response = self.client.post('/api/game/play/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number'], 841)
        self.assertEqual(response.data['result'], 'lose')
        self.assertIsNone(response.data['prize'])
        
        # Check database record
        game_result = GameResult.objects.first()
        self.assertEqual(game_result.user, self.user)
        self.assertEqual(game_result.number, 841)
        self.assertEqual(game_result.result, 'lose')
        self.assertIsNone(game_result.prize)
    
    def test_play_game_invalid_number_too_low(self):
        """Test playing game with number < 1"""
        data = {'number': 0}
        response = self.client.post('/api/game/play/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_play_game_invalid_number_too_high(self):
        """Test playing game with number > 9999"""
        data = {'number': 10000}
        response = self.client.post('/api/game/play/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_play_game_missing_number(self):
        """Test playing game without number"""
        data = {}
        response = self.client.post('/api/game/play/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_play_game_unauthenticated(self):
        """Test playing game without authentication"""
        self.client.force_authenticate(user=None)
        data = {'number': 100}
        response = self.client.post('/api/game/play/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_game_history(self):
        """Test getting game history"""
        # Create some game results
        GameResult.objects.create(user=self.user, number=100, result='win', prize=10.0)
        GameResult.objects.create(user=self.user, number=101, result='lose', prize=None)
        GameResult.objects.create(user=self.user, number=102, result='win', prize=30.6)
        
        response = self.client.get('/api/game/history/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        # Check order (newest first)
        self.assertEqual(response.data[0]['number'], 102)
        self.assertEqual(response.data[1]['number'], 101)
        self.assertEqual(response.data[2]['number'], 100)
    
    def test_game_history_unauthenticated(self):
        """Test getting game history without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/game/history/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GameModelTests(TestCase):
    """Test GameResult model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_game_result_creation(self):
        """Test creating game result"""
        game_result = GameResult.objects.create(
            user=self.user,
            number=500,
            result='win',
            prize=150.0
        )
        
        self.assertEqual(game_result.user, self.user)
        self.assertEqual(game_result.number, 500)
        self.assertEqual(game_result.result, 'win')
        self.assertEqual(float(game_result.prize), 150.0)
        self.assertIsNotNone(game_result.created_at)
    
    def test_game_result_string_representation(self):
        """Test string representation of game result"""
        game_result = GameResult.objects.create(
            user=self.user,
            number=500,
            result='win',
            prize=150.0
        )
        
        expected = f"{self.user.username} - 500 - win"
        self.assertEqual(str(game_result), expected)
    
    def test_game_result_ordering(self):
        """Test that game results are ordered by creation date (newest first)"""
        # Create results in reverse order
        GameResult.objects.create(user=self.user, number=100, result='win', prize=10.0)
        GameResult.objects.create(user=self.user, number=200, result='lose', prize=None)
        
        results = GameResult.objects.all()
        self.assertEqual(results[0].number, 200)  # Newest first
        self.assertEqual(results[1].number, 100)  # Oldest last
