from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from django.db.models import Sum, Count
from django_ratelimit.decorators import ratelimit
from .serializers import GamePlaySerializer, GameResultSerializer
from .models import GameResult
from .consumers import GameConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

def calculate_prize(number):
    """Calculate prize based on number value"""
    if number > 900:
        return round(number * 0.70, 2)
    elif number > 600:
        return round(number * 0.50, 2)
    elif number > 300:
        return round(number * 0.30, 2)
    else:
        return round(number * 0.10, 2)

@extend_schema(
    tags=['Game'],
    summary='Play the number game',
    description='Submit a number and get game result with prize calculation',
    examples=[
        OpenApiExample(
            'Win example (even number)',
            value={'number': 842},
            status_codes=['200'],
            description='Even numbers result in a win with prize'
        ),
        OpenApiExample(
            'Lose example (odd number)',
            value={'number': 841},
            status_codes=['200'],
            description='Odd numbers result in a loss with no prize'
        )
    ],
    responses={
        200: GamePlaySerializer,
        400: GamePlaySerializer,
        401: None,
        429: None
    }
)
@ratelimit(key='user', rate='10/m', method='POST')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def play_game(request):
    """API endpoint for playing the game"""
    serializer = GamePlaySerializer(data=request.data)
    if serializer.is_valid():
        number = serializer.validated_data['number']
        
        # Determine if it's a win (even number) or lose (odd number)
        is_even = number % 2 == 0
        result = 'win' if is_even else 'lose'
        prize = calculate_prize(number) if is_even else None
        
        # Save game result
        game_result = GameResult.objects.create(
            user=request.user,
            number=number,
            result=result,
            prize=prize
        )
        
        # Prepare response data
        response_data = {
            'number': number,
            'result': result,
            'prize': prize
        }
        
        # Send result via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{request.user.id}",
            {
                "type": "game.result",
                "message": response_data
            }
        )
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=['Game'],
    summary='Get game history',
    description='Retrieve the last 3 game results for the current user',
    responses={
        200: GameResultSerializer(many=True),
        401: None
    }
)
@ratelimit(key='user', rate='30/m', method='GET')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def game_history(request):
    """Get user's game history"""
    results = GameResult.objects.filter(user=request.user)[:3]  # Last 3 games
    serializer = GameResultSerializer(results, many=True)
    return Response(serializer.data)

@extend_schema(
    tags=['Game'],
    summary='Get user statistics',
    description='Retrieve comprehensive statistics for the current user',
    responses={
        200: {
            'type': 'object',
            'properties': {
                'total_games': {'type': 'integer'},
                'wins': {'type': 'integer'},
                'losses': {'type': 'integer'},
                'win_rate': {'type': 'number'},
                'total_prize': {'type': 'number'},
                'average_prize': {'type': 'number'},
                'best_prize': {'type': 'number'},
                'last_played': {'type': 'string', 'format': 'date-time'}
            }
        },
        401: None
    }
)
@ratelimit(key='user', rate='20/m', method='GET')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_statistics(request):
    """Get user's game statistics"""
    user_results = GameResult.objects.filter(user=request.user)
    total_games = user_results.count()
    
    if total_games > 0:
        wins = user_results.filter(result='win').count()
        total_prize = user_results.filter(result='win').aggregate(
            total=Sum('prize')
        )['total'] or 0
        best_prize = user_results.filter(result='win').aggregate(
            best=Sum('prize')
        )['best'] or 0
        last_played = user_results.first().created_at
        
        stats = {
            'total_games': total_games,
            'wins': wins,
            'losses': total_games - wins,
            'win_rate': round((wins / total_games * 100), 2),
            'total_prize': float(total_prize),
            'average_prize': round(float(total_prize / wins), 2) if wins > 0 else 0,
            'best_prize': float(best_prize),
            'last_played': last_played.isoformat() if last_played else None
        }
    else:
        stats = {
            'total_games': 0,
            'wins': 0,
            'losses': 0,
            'win_rate': 0,
            'total_prize': 0,
            'average_prize': 0,
            'best_prize': 0,
            'last_played': None
        }
    
    return Response(stats)
