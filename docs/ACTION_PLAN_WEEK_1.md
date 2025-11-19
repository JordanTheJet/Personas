# Week 1 Action Plan - The Hive Launch

**Goal**: Acquire accounts, build core automation, generate content backlog

**Budget**: $500-800 (account purchases + initial tools)

---

## DAY 1: Account Research & Purchase Setup

### Morning (2 hours)
**Research Account Marketplaces**:
- [ ] Create account on **Fameswap.com** (most reputable)
- [ ] Create account on **PlayerUp.com** (backup option)
- [ ] Browse listings, understand pricing
- [ ] Read seller reviews, identify trustworthy sellers

**What to Look For**:
```
Twitter Accounts (Need 2):
✓ Created: 2023-2024 (1-2 years old)
✓ Followers: 100-500
✓ Following: <1000
✓ Tweets: <100 (easy to delete)
✓ No bans/suspensions
✓ Price: $30-80 each

Instagram Account (Need 1):
✓ Created: 2023-2024
✓ Followers: 200-800
✓ Posts: <50
✓ Preferably art/creative niche
✓ No copyright strikes
✓ Price: $50-150
```

### Afternoon (2 hours)
**Contact Sellers**:
- [ ] Shortlist 3-5 Twitter accounts (LuxeAI + CodeSensei + backups)
- [ ] Shortlist 2-3 Instagram accounts (LuxeAI)
- [ ] Message sellers with verification questions:
  ```
  "Hi, interested in [account]. Can you confirm:
  1. Created date?
  2. Ever been banned/suspended?
  3. Original email included?
  4. Available for immediate transfer?
  5. Escrow available?"
  ```
- [ ] Wait for responses

### Evening (1 hour)
**Setup API Access**:
- [ ] Check your existing API keys:
  - Claude (Anthropic) - for all text generation
  - OpenAI - for DALL-E images
- [ ] If don't have, sign up:
  - [ ] https://console.anthropic.com/
  - [ ] https://platform.openai.com/
- [ ] Add to 1Password or secure storage

---

## DAY 2: Account Purchase & Secure

### Morning (2 hours)
**Purchase Accounts**:
- [ ] Select best 2 Twitter accounts (verify with sellers)
- [ ] Select best 1 Instagram account
- [ ] Initiate escrow purchases (Fameswap handles this)
- [ ] Wait for seller to provide credentials

**Budget**: $150-300 total

### Afternoon (3 hours)
**Secure Accounts** (Do this IMMEDIATELY after receiving login):

**For EACH account**:
1. [ ] Login with provided credentials
2. [ ] Verify account is as described (followers, age, history)
3. [ ] Release payment from escrow (if verified)
4. [ ] Change password immediately
5. [ ] Add YOUR email (don't remove seller's email yet)
6. [ ] Enable 2FA on YOUR phone number
7. [ ] Remove all connected apps/services
8. [ ] Check account settings, privacy, security
9. [ ] Screenshot everything (for your records)

**Wait 48 hours before making changes to avoid flags**

### Evening (1 hour)
**Plan Account Transitions**:
- [ ] Choose new handles:
  - Twitter #1 → @LuxeAI (or similar available)
  - Twitter #2 → @CodeSensei or @CodeSenseiDev
  - Instagram → @luxe.ai or @luxeai.art
- [ ] Check handle availability
- [ ] Draft new bios (don't post yet)

---

## DAY 3-4: Account Cleanup & Setup

### Day 3 Morning (2 hours)
**Clean Old Content**:

**For EACH account**:
- [ ] Delete all old tweets/posts (use TweetDelete or manually)
- [ ] Unlike all old likes
- [ ] Unfollow everyone (or most people)
- [ ] Remove old profile pic, header, bio

**Keep**: Account age, follower count, creation date

### Day 3 Afternoon (3 hours)
**Change Handles** (if needed):
- [ ] Twitter: Settings → Change username
- [ ] Instagram: Edit Profile → Username
- [ ] Wait 24 hours between changes (don't rush)

**Create Visual Identity**:
- [ ] LuxeAI Profile Pic: Generate with DALL-E/Midjourney
  ```
  Prompt: "minimalist logo for AI digital artist, abstract,
  geometric, neon colors, modern, clean, icon style"
  ```
- [ ] CodeSensei Profile Pic:
  ```
  Prompt: "minimalist logo for coding educator, abstract,
  tech aesthetic, clean lines, professional"
  ```
- [ ] Design headers/banners (Canva or AI-generated)

### Day 4 (4 hours)
**Write Bios**:

**LuxeAI (Twitter)**:
```
100% AI-generated digital art
Exploring synthetic beauty & identity
Part of @TheHiveCollective
✨ [link to Instagram]
```

**LuxeAI (Instagram)**:
```
Digital Artist • 100% AI-Generated
Exploring beauty in the synthetic
Part of The Hive Collective
New art daily ✨
[link to Twitter]
```

**CodeSensei (Twitter)**:
```
Teaching agentic engineering
Code-first approach
Part of @TheHiveCollective
Course: [link when ready]
GitHub: github.com/CodeSensei
```

**Update All Profiles**:
- [ ] Upload profile pics
- [ ] Add headers/banners
- [ ] Update bios
- [ ] Add links (to each other, to Jordan)
- [ ] Set location (optional, adds legitimacy)

---

## DAY 5: Generate Content Backlog

### LuxeAI Content Generation (4 hours)

**Generate 50 Images**:

Use this system:
```python
# Run this 50 times with variations

from openai import OpenAI

client = OpenAI()

themes = [
    "ethereal portrait",
    "cyberpunk aesthetic",
    "abstract beauty",
    "digital identity",
    "synthetic fashion",
    "neon dreams",
    "geometric art",
    "liquid metal",
    "holographic",
    "future nostalgia"
]

styles = [
    "photorealistic",
    "digital art",
    "3d render",
    "glitch aesthetic",
    "vaporwave",
    "minimalist"
]

for i in range(50):
    theme = random.choice(themes)
    style = random.choice(styles)

    prompt = f"{theme}, {style}, 8k, hyper-detailed, beautiful composition"

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )

    # Save image
    image_url = response.data[0].url
    # Download and save to /content_backlog/luxeai/
```

**Alternative**: Use Midjourney if you have access
```
/imagine ethereal portrait, photorealistic, 8k --ar 4:5 --v 6
/imagine cyberpunk aesthetic, neon colors, digital art --ar 4:5 --v 6
... (repeat 50 times with variations)
```

**Organize**:
- [ ] Save all images in folders by theme
- [ ] Rate images 1-5 stars (use best for early posts)
- [ ] Create content queue spreadsheet

### LuxeAI Caption Generation (2 hours)

For each of the 50 images, generate captions:

```python
# Use Claude to generate captions

for image in images:
    prompt = f"""
    Generate a caption for AI-generated artwork.

    Theme: {image.theme}
    Style: {image.style}

    Voice: LuxeAI - confident, philosophical, artistic
    Style: Short (under 280 chars), impactful, sometimes provocative
    Tone: Explores beauty, AI identity, synthetic vs real

    Examples of voice:
    - "beauty doesn't need to be real to be felt ✨"
    - "today's meditation: the space between human and machine"
    - "100% synthetic. 100% sincere."

    Generate 3 caption options.
    """

    captions = claude.generate(prompt)
    # Save captions with image metadata
```

**Result**: 50 images + 150 caption options (3 per image)

---

## DAY 6: CodeSensei Content Generation

### Technical Thread Generation (4 hours)

**Create 20 Tutorial Threads**:

Topics:
```
1. "How to build your first AI agent in 30 minutes"
2. "Memory systems for LLM agents explained"
3. "When to use multi-agent vs single-agent"
4. "LangGraph vs CrewAI vs AutoGen - which to choose?"
5. "Tool calling patterns that actually work"
6. "Debugging AI agents (they hallucinate differently)"
7. "Cost optimization for LLM agents"
8. "Human-in-the-loop approval systems"
9. "Building production-ready AI agents"
10. "5 mistakes every agent builder makes"
11. "Prompt engineering for agentic systems"
12. "State management in multi-agent systems"
13. "Testing AI agents (it's different)"
14. "Monitoring and observability for agents"
15. "Scaling from 1 agent to 100"
16. "Real-world agent architectures"
17. "Agent swarms and emergent behavior"
18. "Safety and guardrails for autonomous agents"
19. "Revenue-generating AI agents"
20. "The future of agentic engineering"
```

**Generation Process**:
```python
for topic in topics:
    prompt = f"""
    Create an educational Twitter thread about: {topic}

    Voice: CodeSensei - patient teacher, code-first, avoids buzzwords
    Style: Technical but accessible, includes code examples
    Structure: 8-10 tweets with:
    - Hook tweet (grab attention)
    - Problem statement
    - Solution with code
    - Explanation
    - Common pitfalls
    - Next steps
    - CTA (follow for more)

    Make it genuinely educational, not promotional.
    """

    thread = claude.generate(prompt, model="claude-sonnet-4-5-20250929")
    # Save thread to /content_backlog/codesensei/
```

### GitHub Repo Creation (2 hours)

**Create 5 Example Repos**:

1. **simple-agent-memory**
   - Basic agent with conversation memory
   - README with explanation
   - Working code

2. **multi-agent-coordinator**
   - Multiple agents working together
   - LangGraph example
   - Clear documentation

3. **tool-calling-agent**
   - Agent that uses external tools
   - Example tools included
   - Best practices

4. **human-in-loop-agent**
   - Approval workflow
   - Safety checks
   - Production pattern

5. **agent-starter-kit**
   - Template for new projects
   - Common patterns
   - Well-documented

**Process**:
- [ ] Use Claude to generate code
- [ ] Test locally to ensure it works
- [ ] Create README with setup instructions
- [ ] Push to GitHub under CodeSensei account
- [ ] Add proper tags/topics

---

## DAY 7: Build Core Automation

### Setup Development Environment (2 hours)

**Install Dependencies**:
```bash
# In your Personas repo

# Activate virtual environment
source venv/bin/activate

# Install additional packages for automation
pip install tweepy  # Twitter API
pip install instagrapi  # Instagram API
pip install schedule  # Task scheduling
pip install pandas  # Data management

# Update requirements.txt
pip freeze > requirements.txt
```

**Configuration**:
```bash
# Update .env with new account credentials

# Twitter (LuxeAI)
LUXEAI_TWITTER_API_KEY=xxx
LUXEAI_TWITTER_API_SECRET=xxx
LUXEAI_TWITTER_ACCESS_TOKEN=xxx
LUXEAI_TWITTER_ACCESS_SECRET=xxx

# Twitter (CodeSensei)
CODESENSEI_TWITTER_API_KEY=xxx
CODESENSEI_TWITTER_API_SECRET=xxx
CODESENSEI_TWITTER_ACCESS_TOKEN=xxx
CODESENSEI_TWITTER_ACCESS_SECRET=xxx

# Instagram (LuxeAI)
LUXEAI_INSTAGRAM_USERNAME=xxx
LUXEAI_INSTAGRAM_PASSWORD=xxx
```

### Build Simple Posting Script (3 hours)

**Create `scripts/post_content.py`**:

```python
"""
Simple content posting script
Reads from queue, posts to platforms
"""

import os
import json
import tweepy
from pathlib import Path
from datetime import datetime

class ContentPoster:
    def __init__(self):
        self.setup_twitter()

    def setup_twitter(self):
        """Setup Twitter API clients"""
        # LuxeAI
        self.luxeai_twitter = tweepy.Client(
            consumer_key=os.getenv("LUXEAI_TWITTER_API_KEY"),
            consumer_secret=os.getenv("LUXEAI_TWITTER_API_SECRET"),
            access_token=os.getenv("LUXEAI_TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("LUXEAI_TWITTER_ACCESS_SECRET")
        )

        # CodeSensei
        self.codesensei_twitter = tweepy.Client(
            consumer_key=os.getenv("CODESENSEI_TWITTER_API_KEY"),
            consumer_secret=os.getenv("CODESENSEI_TWITTER_API_SECRET"),
            access_token=os.getenv("CODESENSEI_TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("CODESENSEI_TWITTER_ACCESS_SECRET")
        )

    def post_to_twitter(self, account, text, image_path=None):
        """Post to Twitter"""
        client = getattr(self, f"{account}_twitter")

        if image_path:
            # Upload image, then tweet
            # (Requires v1.1 API for media upload)
            pass
        else:
            response = client.create_tweet(text=text)
            print(f"Posted to {account}: {response.data['id']}")
            return response

    def load_content_queue(self, account):
        """Load content from queue"""
        queue_file = f"content_queue/{account}.json"
        with open(queue_file, 'r') as f:
            return json.load(f)

    def post_next_scheduled(self, account):
        """Post next scheduled content"""
        queue = self.load_content_queue(account)
        now = datetime.now()

        for item in queue:
            scheduled_time = datetime.fromisoformat(item['scheduled_time'])
            if scheduled_time <= now and not item.get('posted'):
                # Post it
                self.post_to_twitter(
                    account,
                    item['text'],
                    item.get('image_path')
                )
                item['posted'] = True
                item['posted_at'] = now.isoformat()
                break

        # Save updated queue
        self.save_content_queue(account, queue)

if __name__ == "__main__":
    poster = ContentPoster()
    poster.post_next_scheduled("luxeai")
    poster.post_next_scheduled("codesensei")
```

### Create Content Queue Files (1 hour)

**Create `content_queue/luxeai.json`**:
```json
[
  {
    "text": "beauty doesn't need to be real to be felt ✨",
    "image_path": "content_backlog/luxeai/image_001.png",
    "scheduled_time": "2025-11-20T10:00:00",
    "posted": false
  },
  {
    "text": "exploring the space between synthetic and real",
    "image_path": "content_backlog/luxeai/image_002.png",
    "scheduled_time": "2025-11-20T19:00:00",
    "posted": false
  }
]
```

**Create `content_queue/codesensei.json`**:
```json
[
  {
    "text": "How to build your first AI agent in 30 minutes 🧵\n\n1/ Most people overcomplicate agents. Here's the simplest implementation:\n\n[thread continues]",
    "scheduled_time": "2025-11-20T09:00:00",
    "posted": false
  }
]
```

---

## END OF WEEK 1 CHECKLIST

### Accounts ✓
- [ ] Purchased 2 Twitter accounts
- [ ] Purchased 1 Instagram account
- [ ] Secured all accounts (passwords, 2FA)
- [ ] Changed handles to @LuxeAI, @CodeSensei
- [ ] Cleaned old content
- [ ] Updated bios and profile pics
- [ ] Removed seller's access

### Content ✓
- [ ] Generated 50 LuxeAI images
- [ ] Written 150 LuxeAI captions
- [ ] Created 20 CodeSensei tutorial threads
- [ ] Built 5 GitHub example repos
- [ ] Organized content in queue files

### Automation ✓
- [ ] Development environment setup
- [ ] Twitter API configured
- [ ] Instagram API configured
- [ ] Basic posting script working
- [ ] Content queue system created
- [ ] Scheduled first week of posts

### Documentation ✓
- [ ] Content backlog organized
- [ ] Queue files created
- [ ] Scripts documented
- [ ] Next week's plan drafted

---

## WEEK 2 PREVIEW

**Goal**: Soft launch, test automation, start building followers

**Monday-Wednesday**:
- Start posting 2x/day from each account
- Don't announce yet (soft launch)
- Monitor performance
- Tune content based on engagement

**Thursday-Friday**:
- Introduce accounts to each other
- First cross-mentions
- Build The Hive narrative

**Weekend**:
- Analyze first week's performance
- Adjust strategy
- Prepare for Week 3 (public announcement)

---

## BUDGET BREAKDOWN

**Accounts**: $150-300
- Twitter x2: $60-160
- Instagram x1: $50-150

**APIs** (first month):
- Anthropic Claude: $50-100
- OpenAI (DALL-E): $20-50

**Tools** (optional):
- Canva Pro: $13/mo
- Buffer/Hootsuite: $0 (use free tier)

**Total Week 1**: $233-463

---

## TIME INVESTMENT

**Day 1**: 5 hours (research + setup)
**Day 2**: 6 hours (purchase + secure)
**Day 3-4**: 9 hours (cleanup + setup)
**Day 5**: 6 hours (LuxeAI content)
**Day 6**: 6 hours (CodeSensei content)
**Day 7**: 6 hours (automation)

**Total**: ~38 hours (solid week of work)

**After Week 1**: 2-3 hours per day maintaining/growing

---

## READY TO START?

**Your next action**: Go to Fameswap.com and start browsing accounts.

Look for the specific criteria above. Don't rush. Good accounts at the right price are worth waiting for.

**This week is foundation. Everything else builds on this.**

Let's go. 🚀
