# NumberPlay - Django Backend API

A Django REST API with user authentication and real-time WebSocket interaction for a number guessing game.

## Features

- **User Registration & Authentication**: Custom user model with email-based login
- **Real-time Game**: WebSocket-based number game with instant results
- **Prize System**: Dynamic prize calculation based on number ranges
- **Email Notifications**: Welcome emails sent via Celery (mocked for development)
- **REST API**: Clean API endpoints for frontend integration

## Game Rules

- Enter a number between 1-9999
- **Even numbers = WIN** 🎉
- **Odd numbers = LOSE** 😔
- **Prize calculation for wins:**
  - Numbers > 900: 70% of number
  - Numbers > 600: 50% of number  
  - Numbers > 300: 30% of number
  - Numbers ≤ 300: 10% of number

## Technical Stack

- **Backend**: Django 4.2.7
- **API**: Django REST Framework
- **Real-time**: Django Channels + WebSocket
- **Task Queue**: Celery + Redis
- **Database**: SQLite (development)
- **ASGI Server**: Daphne
- **Frontend**: Next.js (separate repository)

## Installation & Setup

### Prerequisites

- Python 3.10+
- Redis server
- Virtual environment

### 1. Clone and Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start Redis Server

```bash
# Install Redis (Ubuntu/Debian)
sudo apt-get install redis-server

# Start Redis
redis-server
```

### 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Start Services

**Terminal 1 - Django ASGI Server (Daphne):**
```bash
daphne -b 0.0.0.0 -p 8000 numberplay.asgi:application
```

**Terminal 2 - Celery Worker:**
```bash
celery -A numberplay worker --loglevel=info
```

**Terminal 3 - Celery Beat (optional, for scheduled tasks):**
```bash
celery -A numberplay beat --loglevel=info
```

## API Endpoints

### Authentication
- `POST /auth/api/register/` - User registration
- `POST /auth/api/login/` - User login

### Game
- `POST /api/game/play/` - Play the game
- `GET /api/game/history/` - Get game history

### WebSocket
- `ws://localhost:8000/ws/game/` - Real-time game results

## Frontend Integration

This backend is designed to work with a Next.js frontend. The frontend should be configured to:

- Make API calls to `http://localhost:8000`
- Connect to WebSocket at `ws://localhost:8000/ws/game/`
- Handle CORS for cross-origin requests

## Usage

1. **API Integration**: Use the REST API endpoints for authentication and game logic
2. **Play Game**: Go to `/game/` or root URL `/`
3. **Enter Number**: Input a number (1-9999) and click "Play Game"
4. **Real-time Results**: See results appear instantly via WebSocket

## Development

### Project Structure
```
backend/
├── auth_app/          # User authentication
├── game_app/          # Game logic & WebSocket
├── numberplay/        # Main project settings
├── templates/         # HTML templates
├── static/           # Static files
└── manage.py
```

### Key Files
- `numberplay/settings.py` - Django settings
- `numberplay/asgi.py` - ASGI configuration for WebSocket
- `numberplay/celery.py` - Celery configuration
- `auth_app/views.py` - Authentication views
- `game_app/views.py` - Game API views
- `game_app/consumers.py` - WebSocket consumer
- `templates/game_app/game.html` - Game interface

### Environment Variables
Create a `.env` file for production settings:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your-database-url
REDIS_URL=your-redis-url
```

## Testing

```bash
# Run tests
python manage.py test

# Test specific app
python manage.py test auth_app
python manage.py test game_app
```

## Production Deployment

1. Set `DEBUG=False` in settings
2. Configure proper database (PostgreSQL/MySQL)
3. Set up Redis for production
4. Configure email backend
5. Use ASGI server (Daphne) for WebSocket support
6. Set up static file serving

## License

This project is for educational purposes. 