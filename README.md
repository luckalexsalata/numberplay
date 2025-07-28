# NumberPlay

A Django app with user authentication and real-time game interaction via WebSocket.

---

## Screenshots

### Registration Page
![Registration Page](docs/images/registration.png)

### Game Interface
![Game Interface](docs/images/game.png)

---

## Features

- User registration and login (JWT)
- Play a number game: send a number, get instant result
- Real-time results via authenticated WebSocket
- Game history (last 3 results)
- Minimal frontend UI (Next.js)

---

## Main Endpoints

**Auth**
- `POST /auth/api/register/` — Register (username, email, password)
- `POST /auth/api/login/` — Login (email, password)
- `GET /auth/api/user/` — Get current user info

**Game**
- `POST /api/game/play/` — Play game (`{"number": 842}`)
- `GET /api/game/history/` — Last 3 results
- `GET /api/game/statistics/` — User stats

**WebSocket**
- `ws://localhost:8000/ws/game/?token=...` — Real-time game results (JWT required)

**System**
- `GET /health/` — Health check
- `GET /api/docs/` — API docs (Swagger)

---

## Game Logic

- Even number: win, odd: lose
- Prize (if win):
  - >900 — 70%
  - >600 — 50%
  - >300 — 30%
  - ≤300 — 10%
- WebSocket response: `{ "number": 842, "result": "win", "prize": 589.4 }`

---

## Quick Start

```bash
git clone <repo-url>
cd NumberPlay
sudo docker-compose up -d
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

(Optional) Create admin:
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```

---

- Python 3.10+, Django 4.x, DRF, Channels, Celery, Redis, MySQL/SQLite, Daphne, Docker
- All configs are set by default. No manual setup needed. 