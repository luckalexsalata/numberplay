# NumberPlay Frontend

Next.js frontend for the NumberPlay game application.

## Features

- **Modern UI** with Tailwind CSS
- **TypeScript** for type safety
- **WebSocket** real-time communication
- **Responsive design** for all devices
- **Authentication** with Django backend

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Django backend running on port 8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
src/
├── app/                 # Next.js App Router pages
├── components/          # React components
├── hooks/              # Custom React hooks
├── lib/                # Utility functions and API client
└── types/              # TypeScript type definitions
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## API Integration

The frontend communicates with the Django backend via:
- REST API for authentication and game actions
- WebSocket for real-time game results

## Technologies Used

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **WebSocket** - Real-time communication
