from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .tasks import send_welcome_email

@extend_schema(
    tags=['Authentication'],
    summary='Register new user',
    description='Create a new user account with email and password',
    examples=[
        OpenApiExample(
            'Valid registration',
            value={
                'username': 'john_doe',
                'email': 'john@example.com',
                'password': 'SecurePass123',
                'password_confirm': 'SecurePass123'
            },
            status_codes=['201']
        )
    ],
    responses={
        201: UserSerializer,
        400: UserRegistrationSerializer
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    """API endpoint for user registration"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Send welcome email via Celery
        send_welcome_email.delay(user.id)
        
        # Create JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=['Authentication'],
    summary='User login',
    description='Authenticate user and return JWT tokens',
    examples=[
        OpenApiExample(
            'Valid login',
            value={
                'email': 'john@example.com',
                'password': 'SecurePass123'
            },
            status_codes=['200']
        )
    ],
    responses={
        200: UserSerializer,
        400: UserLoginSerializer
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    """API endpoint for user login"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Create JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=['Authentication'],
    summary='Get current user info',
    description='Retrieve information about the currently authenticated user',
    responses={
        200: UserSerializer,
        401: None
    }
)
@api_view(['GET'])
def get_user_info(request):
    """Get current user info"""
    return Response({
        'user_id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })
