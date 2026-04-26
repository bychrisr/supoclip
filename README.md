# Fuck OpusClip.

... because good video clips shouldn't cost a fortune or come with ugly watermarks.

OpusClip charges $15-29/month and slaps watermarks on every free video. SupoClip gives you the same AI-powered video clipping capabilities - completely free, completely open source, and completely watermark-free, while still providing you with a hosted version, that doesn't cost the same amount as your mortgage.

> For the hosted version, sign up for the waitlist here: [SupoClip Hosted](https://supoclip.vercel.app)

## Why SupoClip Exists

### The OpusClip Problem

OpusClip is undeniably powerful. It's an AI video clipping tool that can turn long-form content into viral short clips with features like:

- AI-powered clip generation from long videos
- Automated captions with 97%+ accuracy
- Virality scoring to predict viral potential
- Multi-language support (20+ languages)
- Brand templates and customization

**But here's the catch:**

- **Free plan limitations**: Only 60 minutes of processing per month
- **Watermarks everywhere**: Every free video gets branded with OpusClip's watermark
- **Expensive pricing**: $15/month for Starter, $29/month for Pro
- **Processing limits**: Even paid plans have strict minute limits
- **Vendor lock-in**: Your content and workflows are tied to their platform

### The SupoClip Solution

SupoClip provides the same core functionality without the financial burden:

→ ✅ **Completely Free** - No monthly fees, no processing limits

→ ✅ **No Watermarks** - Your content stays yours

→ ✅ **Open Source** - Full transparency, community-driven development

→ ✅ **Self-Hosted** - Complete control over your data and processing

→ ✅ **Unlimited Usage** - Process as many videos as your hardware can handle

→ ✅ **Customizable** - Modify and extend the codebase to fit your needs

## Features

- 🎥 **AI Video Clipping**: Smart engagement detection using Gemini or AssemblyAI.
- 💬 **Animated Captions (v2)**: High-performance, unified rendering engine (MoviePy v2) with `pop`, `bounce`, and `fade` effects.
- 🛡️ **YouTube Resilience**: Built-in **Proxy Rotation** and **User Cookie Bypass** via Settings UI.
- ⚡ **Real-time Progress**: Server-Sent Events (SSE) for granular task monitoring.
- 🎨 **Dynamic Templates**: Preset styles (TikTok, MrBeast, Hormozi) with word-level highlighting.
- 🛠️ **Manual Editor**: Trim, split, and merge clips with custom fonts and multiple aspect ratios (9:16, 1:1, 4:5).
- 🔐 **Secure & Private**: Cookies and credentials are treated with enterprise-grade security.

## Quick Start

### Prerequisites

- Docker and Docker Compose
- An AssemblyAI API key (v0.63.0+ compatible) - [Get one here](https://www.assemblyai.com/)
- An LLM provider for AI analysis - OpenAI, Google, Anthropic, or Ollama

### 1. Clone and Configure

```bash
git clone https://github.com/your-username/supoclip.git
cd supoclip
```

Create a `.env` file in the root directory:

```env
# Required: Video transcription
ASSEMBLY_AI_API_KEY=your_assemblyai_api_key

# Required: Choose ONE LLM provider and set its API key
LLM=google-gla:gemini-3-flash-preview
GOOGLE_API_KEY=your_google_api_key

# Optional: YouTube Bypass (Proxies)
PROXY_LIST=http://user:pass@ip:port
PROXY_SERVICE_URL=http://your-proxy-service.com

# Optional: Auth secret (change in production)
BETTER_AUTH_SECRET=change_this_in_production
```

### 2. Start the Services

```bash
docker-compose up -d
```

### 3. Setup YouTube Cookies (Recommended)

To avoid "Video Unavailable" errors, go to `http://localhost:3000/settings` and paste your YouTube cookies in Netscape format.

## Testing

Comprehensive test suites are included for all core components:

```bash
cd backend
uv run pytest
```

See [TESTING.md](TESTING.md) for details on unit, integration, and performance tests.

## License

SupoClip is released under the AGPL-3.0 License. See [LICENSE](LICENSE) for details.
