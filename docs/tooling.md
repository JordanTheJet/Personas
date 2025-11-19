# Complete Tooling Stack

**Last Updated: November 19, 2025** - Reflects current AI models, tools, and pricing

## Overview

This document outlines every tool, service, and integration needed to build and operate the AI Agent Collective. Tools are categorized by function and include specific recommendations, pricing, and integration complexity.

**Major 2025 Updates:**
- Claude Sonnet 4.5, Opus 4, Haiku 4 (30% cheaper, better performance)
- GPT-5.1 (significant reasoning improvements)
- Midjourney V7 Official API
- Sora public release (game-changing video generation)
- DALL-E 4 (50% cheaper)
- ElevenLabs V3, Suno V4 (professional quality audio)
- All pricing and capabilities updated for late 2025

---

## 1. Core Agent Infrastructure (2025 Updates)

### Agent Framework & Orchestration

**Option A: LangGraph** ⭐ Recommended for MVP (2025)
- **What**: Production-ready agent framework (evolved from LangChain)
- **Why**: Built for agentic workflows, state graphs, human-in-loop
- **Cost**: Free (open source) + optional LangSmith ($39+/mo for monitoring)
- **Complexity**: Medium
- **Install**: `pip install langgraph langchain-anthropic`
- **2025 Update**: Now industry standard for agent orchestration

**Option B: CrewAI** ⭐ Great for Multi-Agent Systems
- **What**: Purpose-built for AI agent crews
- **Why**: Simple multi-agent coordination, role-based agents
- **Cost**: Free (open source)
- **Complexity**: Low-Medium
- **Install**: `pip install crewai crewai-tools`
- **When**: If you want simpler multi-agent setup

**Option C: AutoGen Studio** (Microsoft)
- **What**: Multi-agent conversation framework + UI
- **Why**: Good for agent-to-agent conversation, visual workflow builder
- **Cost**: Free (open source)
- **Complexity**: Medium
- **Install**: `pip install autogen-studio`

**Option D: Custom Framework**
- **What**: Build from scratch
- **Why**: Full control, optimized for your use case
- **Cost**: Free (development time)
- **Complexity**: High
- **When**: After validating with LangGraph/CrewAI

**Recommended (2025)**: Start with **LangGraph** for production-ready features or **CrewAI** for simpler multi-agent coordination.

### Task Scheduling & Automation

**Celery + RabbitMQ** ⭐ Recommended
- **What**: Distributed task queue
- **Why**: Reliable, scalable, Python-native
- **Cost**: Free (open source)
- **Setup**:
  ```bash
  pip install celery
  docker run -d -p 5672:5672 rabbitmq:3
  ```

**Alternative: APScheduler**
- Simpler, good for single-server setup
- `pip install apscheduler`

### Memory & State Management

**PostgreSQL** (Structured Data) ⭐
- **What**: Relational database
- **Why**: Reliable, full-featured
- **Cost**: Free (self-hosted) or $7+/mo (managed)
- **Setup**: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=pwd postgres`

**Redis** (Cache & Sessions) ⭐
- **What**: In-memory data store
- **Why**: Fast caching, pub/sub
- **Cost**: Free (self-hosted) or $5+/mo (managed)
- **Setup**: `docker run -d -p 6379:6379 redis`

**Vector Database** (Embeddings & Memory) ⭐
- **Pinecone**: Managed, easy ($70+/mo for production)
- **Weaviate**: Self-hosted, free (docker)
- **ChromaDB**: Simple, embedded (`pip install chromadb`)

**Recommended**: ChromaDB for MVP, Pinecone for production.

---

## 2. AI & Language Models (Updated November 2025)

### Large Language Models

**Anthropic Claude** ⭐ Primary
- **Models** (Current as of Nov 2025):
  - Claude Sonnet 4.5 (best balance, latest flagship)
  - Claude Opus 4 (maximum capability, complex reasoning)
  - Claude Haiku 4 (fast, efficient, cost-effective)
- **Cost** (2025 pricing):
  - Sonnet 4.5: $2/M input, $10/M output tokens (30% cheaper than 3.5)
  - Opus 4: $12/M input, $60/M output
  - Haiku 4: $0.15/M input, $0.75/M output
- **API**: `pip install anthropic` (latest SDK)
- **Why**: Best for agentic workflows, coding, extended context (500K+ tokens), computer use
- **New Features**: Native tool use, improved function calling, multi-modal vision

**OpenAI GPT-5** (Strong Alternative)
- **Models**: GPT-5.1, GPT-5.1-mini
- **Cost**: $1.50-8/M input tokens (competitive with Claude)
- **API**: `pip install openai` (v2.0+ SDK)
- **Why**: Excellent reasoning, multimodal, fast inference
- **New Features**: Better context retention, improved coding, native structured outputs

**Google Gemini 2.0** (Emerging)
- **Models**: Gemini 2.0 Ultra, Pro
- **Cost**: $1-5/M tokens (very competitive)
- **Why**: Strong multimodal, good for vision tasks
- **Use Case**: Image/video understanding

**Budget Considerations** (2025):
- Start with Haiku 4 for routine tasks (~$20-50/mo per agent)
- Use Sonnet 4.5 for important decisions (~$100-200/mo per agent)
- Reserve Opus 4 for complex reasoning only
- Estimated: $75-400/mo per active agent (better performance, lower cost vs 2024)

### Image Generation (2025 Updates)

**Midjourney V7** ⭐ Still Best for Aesthetics
- **Access**: Official API now available! (launched mid-2025)
- **Cost**: $30-120/mo subscription + $0.02-0.08/image via API
- **Quality**: Photorealistic, artistic excellence
- **Speed**: Fast (3-8 seconds)
- **API**: Official REST API - `pip install midjourney-api`
- **Why**: Unmatched aesthetic quality, consistent style

**DALL-E 4** (OpenAI) ⭐ Most Versatile
- **Access**: Official API in GPT-5 ecosystem
- **Cost**: $0.02-0.06 per image (50% cheaper than DALL-E 3)
- **Quality**: Excellent, better text rendering
- **Speed**: Very fast (2-5 seconds)
- **API**: Built into OpenAI SDK v2
- **Why**: Easy integration, great for iteration

**Flux Pro 2.0** (Black Forest Labs) ⭐ Rising Star
- **Access**: API or self-hosted
- **Cost**: $0.01-0.04/image (API) or GPU costs (self-host)
- **Quality**: Rivals Midjourney, better prompt adherence
- **Speed**: Fast
- **Why**: Open weights, customizable, excellent value

**Stable Diffusion 4 / SDXL Turbo**
- **Access**: Self-hosted (ComfyUI, Auto1111)
- **Cost**: GPU only (~$0.20-0.40/hr on RunPod)
- **Quality**: Excellent with right models
- **Speed**: Very fast with optimizations
- **Why**: Free per-image, full control, LoRA training

**Recommended Stack (2025)**:
- **LuxeAI**: Midjourney V7 (hero content) + Flux Pro (volume) + SD4 (experimentation)
- **PixelPhantom**: DALL-E 4 (sprites, quick iteration) + SD4 (pixel art LoRAs, textures)

### Video Generation (2025 - Major Improvements!)

**Sora** (OpenAI) ⭐ Game Changer
- **Features**: Text/image to 1080p video, up to 60 seconds, realistic physics
- **Cost**: $0.10-0.30/second (cheaper at scale)
- **Quality**: Photorealistic, coherent
- **API**: OpenAI SDK v2
- **Use**: LuxeAI hero content, PixelPhantom trailers
- **Why**: Industry-leading quality, finally publicly available

**Runway Gen-3** ⭐ Professional Grade
- **Features**: Gen-3 Alpha, motion control, multi-shot
- **Cost**: $8-60/mo + $0.03-0.08/second
- **Quality**: Excellent, good for creative control
- **Use**: LuxeAI content creation
- **Why**: Best creative controls, established workflow

**Pika 2.0**
- **Features**: Extended videos, better consistency
- **Cost**: $8-58/mo
- **Quality**: Very good, improving fast
- **Use**: Volume content, experimentation

**Kling AI / Luma Dream Machine**
- **Cost**: $10-40/mo
- **Quality**: Good quality/cost ratio
- **Use**: Budget-friendly alternative

**Recommended Stack (2025)**:
- **Primary**: Sora for quality, Runway for creative control
- **Volume**: Pika or Luma for batch content
- **Cost**: ~$50-200/mo depending on volume

### Audio & Voice (2025 Updates)

**ElevenLabs V3** ⭐ Industry Standard TTS
- **Quality**: Indistinguishable from human, emotion control
- **Cost**: $5-330/mo (50k-3M characters - 50% more included)
- **New Features**: Real-time voice streaming, voice cloning from 10s samples
- **Use**: PixelPhantom narration, LuxeAI voice content, course narration

**Suno V4** ⭐ Music Generation
- **Quality**: Radio-quality full songs
- **Cost**: $10-40/mo
- **New Features**: Extended songs (5+ minutes), stem separation, genre mixing
- **Use**: PixelPhantom game soundtracks, content background music

**Udio Pro** (Strong Alternative)
- **Cost**: $10-30/mo
- **Quality**: Comparable to Suno
- **Use**: Alternative/backup music generation

**OpenAI TTS (GPT-5 Voice)**
- **Cost**: $0.015/1K characters (50% cheaper)
- **Quality**: Excellent, multiple voices
- **Use**: Budget-friendly TTS for high-volume needs

---

## 3. Social Media Integration

### Twitter/X API

**Access Methods**:
1. **Official API** (Expensive)
   - Free tier: Very limited (post only)
   - Basic: $100/mo (read + write)
   - Pro: $5,000/mo (full access)

2. **Unofficial APIs** ⭐ Recommended for MVP
   - `twitter-api-client` (Python)
   - Scrapers with auth
   - Risk: Against TOS, could break

**Features Needed**:
- Post tweets
- Read mentions/replies
- Send DMs
- Get analytics

**Recommended**: Start unofficial, budget for official API later.

### Instagram API

**Official API**:
- Requires Facebook Developer account
- Business/Creator account needed
- Free tier available
- Good documentation

**Features**:
- Post photos/videos
- Respond to comments
- Get insights
- Manage DMs (limited)

**Library**: `instagrapi` (unofficial) or official Graph API

### OnlyFans Integration

**Challenge**: No official API

**Solution Options**:
1. **Browser Automation** (Selenium/Playwright)
   - Automate posting via browser
   - High maintenance

2. **Third-party Tools**
   - Fancentro, LoyalFans (have APIs)
   - Consider alternatives with APIs

3. **Manual Hybrid**
   - AI generates content
   - Manual upload initially
   - Automate DMs and engagement

**Payment Integration**:
- OnlyFans handles payments
- Webhook monitoring for subscriptions

**Recommended**: Start with semi-manual, explore automation carefully.

### YouTube

**Official API**: Excellent
- **Cost**: Free (with quotas)
- **Features**: Upload, manage, analytics
- **Library**: `google-api-python-client`

**Use Case**: PixelPhantom dev vlogs (generated videos)

### TikTok

**Official API**: Limited
- Requires business account
- Posting in beta

**Alternatives**:
- Manual posting initially
- Use unofficial tools cautiously

### Discord

**Official API**: Excellent
- **Cost**: Free
- **Library**: `discord.py`
- **Use**: Community management, agent interactions

---

## 4. Development & Code Generation

### AI Coding Tools

**Claude Code** ⭐ Recommended
- **What**: AI pair programmer
- **Cost**: Part of Claude API
- **Use**: PixelPhantom game development

**Cursor**
- **What**: AI-first code editor
- **Cost**: $20/mo Pro
- **Use**: Human development workflow

**GitHub Copilot**
- **Cost**: $10/mo
- **Use**: Supplementary

### Version Control

**GitHub** ⭐
- **Cost**: Free for public repos
- **Features**:
  - Git hosting
  - Actions (CI/CD)
  - Pages (hosting)
  - Releases

**Integration**:
- `PyGithub` library
- Automated commits from agents
- Release automation

### Game Engines

**Godot** ⭐ Recommended for PixelPhantom
- **Why**:
  - Open source
  - Scriptable (GDScript/Python-like)
  - Good for 2D
  - Headless export
- **Cost**: Free
- **Automation**: Command-line build tools

**Pygame** (Alternative)
- Pure Python
- Easier to automate
- Good for simple games

**Unity**
- More powerful
- Harder to automate
- Consider later

---

## 5. Content Management & Distribution

### Game Distribution

**itch.io** ⭐ Perfect for Indie
- **API**: Available
- **Cost**: Free (optional 10% cut)
- **Features**:
  - Easy uploads
  - Built-in payments
  - Community features
- **Library**: Custom API client

**Steam**
- **Cost**: $100 per game fee
- **Complexity**: High (legal requirements)
- **When**: After proven success on itch.io

**Game Jolt**
- Alternative to itch.io
- Good community

### Content Delivery Network

**Cloudflare R2** ⭐
- **What**: S3-compatible storage
- **Cost**: $0.015/GB storage, free egress
- **Use**: Store generated images, videos, game assets

**Alternatives**:
- AWS S3 (more expensive egress)
- Backblaze B2 (cheap)

### Website/Portfolio

**GitHub Pages** ⭐ Free
- **Use**: Agent portfolio sites
- **Tech**: Static site generators (Hugo, Jekyll)

**Vercel/Netlify**
- Easy deployment
- Free tier available

---

## 6. Analytics & Monitoring

### Social Analytics

**Custom Dashboard** ⭐ Recommended
- **Stack**:
  - PostgreSQL (data storage)
  - Metabase/Grafana (visualization)
  - Python scripts (data collection)
- **Metrics**:
  - Follower growth
  - Engagement rates
  - Post performance
  - Revenue (if applicable)

**Third-party Tools**:
- SocialBlade (public data)
- Hootsuite Analytics ($99+/mo)

### Application Monitoring

**Prometheus + Grafana** ⭐
- **What**: Metrics and visualization
- **Cost**: Free (self-hosted)
- **Metrics**:
  - API call rates
  - Response times
  - Error rates
  - Resource usage

**Sentry**
- **What**: Error tracking
- **Cost**: Free tier, then $26+/mo
- **Use**: Catch and track bugs

**Logging: ELK Stack**
- Elasticsearch + Logstash + Kibana
- **Cost**: Free (self-hosted, resource-heavy)
- **Alternative**: Loki + Grafana (lighter)

---

## 7. Infrastructure & Hosting

### Compute

**Option A: VPS** ⭐ Recommended for Start
- **Providers**:
  - DigitalOcean ($12-48/mo)
  - Linode/Akamai ($12-48/mo)
  - Hetzner ($5-20/mo, Europe)
- **Specs**: 4GB+ RAM, 2+ CPUs
- **Why**: Simple, cost-effective

**Option B: Cloud** (AWS/GCP/Azure)
- More complex
- Better scaling
- Higher cost
- Use later if needed

**Option C: Dedicated Server**
- OVH, Hetzner ($30-100/mo)
- More resources
- Good for GPU workloads

### Containers & Orchestration

**Docker** ⭐ Essential
- **Why**: Consistent environments
- **Cost**: Free
- **Use**: Package each agent + services

**Docker Compose** ⭐ Start Here
- **Why**: Multi-container management
- **Cost**: Free
- **Use**: Local dev and small production

**Kubernetes** (Later)
- When you need serious scaling
- Complexity not worth it initially

### GPU Access (for Stable Diffusion)

**RunPod** ⭐ Recommended
- **Cost**: ~$0.20-0.60/hr (pay per use)
- **GPUs**: RTX 3090, A4000, etc.
- **Why**: Cheap, easy

**Vast.ai**
- Community GPU marketplace
- Very cheap ($0.10-0.30/hr)
- Variable availability

**Lambda Labs**
- Good for persistent instances
- $0.50-1.50/hr

---

## 8. Security & Secrets Management

### Secrets Management

**HashiCorp Vault** ⭐ Best Practice
- **What**: Secrets management
- **Cost**: Free (self-hosted)
- **Why**: Secure, audited

**Alternative**: Environment Variables
- Simpler, less secure
- OK for MVP
- Use Docker secrets or `.env` files

### API Gateway & Rate Limiting

**Kong** (Open Source)
- API gateway
- Rate limiting
- Authentication

**Custom with Redis**
- Simpler for small scale
- Rate limit with Redis counters

### Content Moderation

**OpenAI Moderation API** ⭐
- **Cost**: Free
- **Use**: Filter AI-generated content
- **Catches**: Violence, sexual, hate speech

**Custom Filters**
- Keyword blocking
- Image hash checking (prevent duplicates)

---

## 9. Payment & Monetization

### Payment Processing

**Stripe** ⭐ Recommended
- **What**: Payment platform
- **Cost**: 2.9% + $0.30 per transaction
- **Features**:
  - Subscriptions
  - One-time payments
  - Customer management
- **API**: `pip install stripe`

**Use Cases**:
- Patreon alternative
- Tip jar
- Custom subscriptions

### Platform-specific

**OnlyFans**: Handles own payments
**Patreon**: Handles own payments (8-12% fee)
**itch.io**: Handles payments (0-10% optional fee)

---

## 10. Development Tools

### Code & Text Editors

- **VS Code**: Primary IDE
- **Cursor**: AI-enhanced development
- **PyCharm**: Python development

### Testing & QA

**pytest** ⭐
- **What**: Python testing framework
- **Use**: Test agent behaviors

**Playwright**
- **What**: Browser automation
- **Use**: Social media automation testing

### CI/CD

**GitHub Actions** ⭐ Free
- **Use**:
  - Run tests on push
  - Deploy agents automatically
  - Build game releases

---

## 11. Communication & Collaboration

### Team Communication

**Discord** ⭐
- **Use**:
  - Agent logs channel
  - Alerts and monitoring
  - Human oversight notifications

**Slack** (Alternative)
- Better for business
- More expensive

### Documentation

**Notion** or **Obsidian**
- Agent knowledge bases
- Planning documents
- Living documentation

**GitHub Wiki**
- Technical documentation
- Free with repo

---

## Complete Cost Estimate (Updated November 2025)

### Monthly Recurring Costs

**Tier 1: MVP (Single Agent)** - 2025 Pricing
- VPS Hosting: $15-25/mo (VPS prices stable/slightly lower)
- Claude API: $75-150/mo (30% cheaper than 2024)
- Image Generation: $15-40/mo (DALL-E 4 50% cheaper)
- Video (optional): $20-50/mo (Sora/Pika)
- Social Media APIs: $0-50/mo
- Domain: $1/mo
- **Total: $125-280/mo** (15% cheaper than 2024!)

**Tier 2: Full Collective (3 Original Agents)**
- VPS/Cloud: $40-80/mo
- Claude/GPT API: $225-450/mo (better pricing, more efficient models)
- Image Generation: $80-150/mo (Midjourney API + DALL-E 4)
- Video Generation: $50-150/mo (Sora + Runway)
- Audio/Music: $25-50/mo (ElevenLabs V3 + Suno V4)
- Social APIs: $50-150/mo (better unofficial tools available)
- Storage (CDN): $10-20/mo
- Monitoring/Tools: $20-50/mo
- **Total: $500-1,100/mo** (20% cheaper with better quality!)

**Tier 3: Full Collective (6 Agents - Original 3 + New Course Creators)**
- Infrastructure: $80-150/mo
- AI APIs: $450-900/mo (6 agents, efficient usage)
- Content Gen (all types): $200-400/mo
- Course Platforms: $50-100/mo (Teachable, Gumroad, etc.)
- Email/Marketing: $30-80/mo
- All other integrations: $100-200/mo
- **Total: $910-1,830/mo**

**Tier 4: Production Scale (6 Agents + Revenue)**
- Infrastructure: $150-400/mo
- AI APIs: $800-1,500/mo
- All content generation: $300-600/mo
- Marketing & Tools: $150-300/mo
- Platform fees: Varies (% of revenue)
- Buffer for experiments: $200/mo
- **Total: $1,600-3,000/mo**

**Note**: 2025 brings better performance at lower cost. Same quality output costs ~20-30% less than 2024.

### One-time Costs

- Domain registration: $10-15/yr
- Steam developer fee: $100 (if/when)
- Legal (LLC setup): $100-500 (optional)

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)

**Infrastructure**:
- [ ] Set up VPS/cloud instance
- [ ] Deploy PostgreSQL + Redis
- [ ] Configure Docker environment
- [ ] Set up monitoring basics

**Core Framework**:
- [ ] Install LangChain/LangGraph
- [ ] Build base agent class
- [ ] Implement memory system
- [ ] Create task scheduler

**First Integration**:
- [ ] Claude API integration
- [ ] Twitter API (unofficial)
- [ ] Basic content generation

**Deliverable**: JordanTheJet augmentation system working

### Phase 2: First Agent (Weeks 5-8)

**Choose**: PixelPhantom OR LuxeAI (easier to start)

**Build**:
- [ ] Persona implementation
- [ ] Content generation pipeline
- [ ] Social media automation
- [ ] Analytics dashboard

**If PixelPhantom**:
- [ ] Game engine integration
- [ ] Asset generation pipeline
- [ ] itch.io deployment

**If LuxeAI**:
- [ ] Image generation workflow
- [ ] Multi-platform posting
- [ ] Engagement automation

**Deliverable**: One fully autonomous agent running

### Phase 3: Scale & Refine (Weeks 9-12)

**Build Second Agent**:
- [ ] Implement remaining agent
- [ ] Test inter-agent communication
- [ ] Refine based on learnings

**Optimization**:
- [ ] Reduce API costs
- [ ] Improve content quality
- [ ] Enhance autonomy

**Community**:
- [ ] Build documentation
- [ ] Share learnings publicly
- [ ] Grow agent audiences

**Deliverable**: Full collective operational

---

## Essential Tools Summary

### Must-Have (Day 1)
1. Claude API (Anthropic)
2. PostgreSQL + Redis
3. Python 3.11+
4. Docker
5. Git/GitHub
6. VPS hosting

### Critical (Week 1)
7. LangChain
8. Twitter API access
9. DALL-E 3 or Midjourney
10. Monitoring setup (basic)

### Important (Month 1)
11. Celery + RabbitMQ
12. Vector database (ChromaDB)
13. Instagram API
14. Sentry error tracking
15. Content moderation

### Nice-to-Have (Month 2+)
16. Video generation (Runway)
17. Audio (ElevenLabs, Suno)
18. Advanced analytics
19. Multi-platform expansion
20. Custom optimizations

---

## Recommended Tech Stack (Final)

**Core**:
- Python 3.11+
- LangChain + LangGraph
- PostgreSQL + Redis + ChromaDB
- Celery + RabbitMQ
- Docker + Docker Compose

**AI Services**:
- Claude 3.5 Sonnet (primary LLM)
- DALL-E 3 + Midjourney (images)
- Runway ML (video)
- ElevenLabs (audio)

**Social**:
- Twitter API (unofficial → official)
- Instagram Graph API
- Discord.py

**Infrastructure**:
- DigitalOcean/Hetzner VPS
- Cloudflare R2 (storage)
- GitHub (code + actions)
- Prometheus + Grafana (monitoring)

**Development**:
- VS Code + Cursor
- pytest
- GitHub Actions
- Sentry

This stack balances capability, cost, and complexity for getting started while allowing scaling later.
