# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Voither landing page - a Vite-based TypeScript application for an AI-Native Private Edge Cloud platform for healthcare. The site showcases Voither's technology stack including HealthOS, Mestral Engine, and Sortio platform.

## Development Commands

```bash
# Install dependencies
npm install

# Start development server (port 3000)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Cloudflare Pages deployment
npm run deploy              # Deploy to Cloudflare Pages
npm run deploy:prod         # Deploy to production environment
npm run wrangler:dev        # Test locally with Wrangler (port 8788)
npm run wrangler:login      # Authenticate with Cloudflare
npm run wrangler:publish    # Publish to specific project
```

## Environment Setup

- Create `.env.local` and set `GEMINI_API_KEY` for the AI chatbot functionality
- The app runs on port 3000 by default (configured in vite.config.ts)
- For Cloudflare deployment, set secrets via: `wrangler secret put GEMINI_API_KEY`

## Cloudflare Pages Integration

- **wrangler.toml** - Cloudflare Worker configuration
- **src/worker.ts** - Worker script for static hosting with API endpoints
- **_routes.json** - Route configuration for Pages
- **dist/** - Build output directory for deployment

## Architecture

### Core Technologies
- **Vite** - Build tool and dev server
- **TypeScript** - Primary language
- **Vanilla JavaScript** - No frontend framework, pure DOM manipulation
- **Google Gemini AI** - Powers chatbot and FAQ functionality
- **Lucide Icons** - Icon library loaded via CDN

### File Structure
- `index.html` - Main HTML template with component structure
- `index.tsx` - Main TypeScript application file with all JavaScript logic
- `index.css` - Global styles and CSS variables
- `vite.config.ts` - Vite configuration
- `package.json` - Dependencies and scripts
- `metadata.json` - Application metadata

### Key Features
- **Feature Flags** - Configurable via `featureFlags` object in index.tsx
- **Internationalization** - English/Portuguese support via `translations` object
- **Interactive Components**:
  - Chatbot powered by Google Gemini AI
  - Interactive FAQ system
  - Technology diagram with modal explanations
  - Contact form
  - Mobile-responsive sidebar navigation

### Architecture Patterns
- **Component-based structure** - Each section is modular
- **Event-driven interactions** - Uses addEventListener patterns
- **CSS Grid/Flexbox** - Modern layout techniques
- **Glass morphism design** - `.glass-card` components throughout
- **Responsive design** - Mobile-first approach with sidebar navigation

## Important Implementation Details

### Chatbot Integration
- Uses Google Gemini 2.5-flash model
- System instruction defines Voither-specific knowledge
- Chat state managed in `chat` variable
- Messages handled via `addMessage()` function

### Feature Flag System
- Toggle features via `featureFlags` object
- Local storage overrides available (`ff_${flagName}`)
- Controls visibility of sections like chatbot and pioneers section

### Internationalization
- Content stored in `translations` object (en/pt)
- Language switching handled by `setLanguage()` function
- Uses `data-key` attributes for translatable content

### Modal System
- Technology diagram modals via `setupInfoModal()`
- Content mapping in `modalContent` object
- Supports keyboard navigation (Escape to close)

## Styling Guidelines

- Uses CSS custom properties (variables) for theming
- Glass morphism aesthetic with transparency effects
- Responsive breakpoints handled via CSS media queries
- Font stack: Roboto (primary), with specialized fonts for headings
- Color scheme stored in CSS variables (light theme default)

## Development Notes

- All JavaScript is in a single file (`index.tsx`) within DOMContentLoaded listener
- No build step required for development beyond Vite
- TypeScript configured for modern ES2022 target
- Uses ES modules with import maps for external dependencies