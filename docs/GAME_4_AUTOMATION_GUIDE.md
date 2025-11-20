# Game #4 Complete Automation Guide

**Goal**: Ship a complete indie game with 90% automation from design → code → assets → video → marketing

**Timeline**: 4-6 weeks (20-30 hours human time, rest automated)

**Human Input Required**:
- Initial game design decisions (2-3 hours)
- Code review and iteration (5-10 hours)
- Final testing and polish (3-5 hours)
- Strategic decisions on marketing

**Everything Else**: Automated

---

## Step 1: Design the Game (Creative Work)

**Human Time**: 2-3 hours
**Automation Level**: 0% (This is where YOU add value)

### What You Decide

The three things only you can decide:

1. **Core Concept**: What's the hook? What makes this different?
2. **Game Feel**: Jump height, gravity, player speed, difficulty curve
3. **Polish Direction**: What makes it feel "juicy" and satisfying?

### Create DESIGN.md Template

Create `games/game_04/DESIGN.md`:

```markdown
# Game #4: Neon Descent

## Core Concept
**Genre**: Vertical platformer (falling downward)
**Hook**: You fall DOWN through neon-lit procedural levels. The longer you survive, the faster you fall.
**Core Loop**: Fall → Dodge obstacles → Collect powerups → Survive longer → Beat high score

## Player Experience
- **Feeling**: Fast, twitchy, "one more run" arcade action
- **Difficulty**: Easy to learn, hard to master
- **Session Length**: 30 seconds to 3 minutes per run
- **Progression**: High score based, unlock new visual themes

## Mechanics (The Three Key Decisions)

### 1. Game Feel
```
Player:
- Width: 32px
- Height: 48px
- Horizontal speed: 300 px/s
- Fall speed: Starts at 200px/s, increases to 800px/s over 60 seconds
- Acceleration: Smooth ease-in-out (not instant)

Controls:
- Left/Right arrows or A/D
- Optional: Mouse/touch for mobile later
```

### 2. Difficulty Curve
```
0-10 seconds: Gentle, wide platforms, slow fall speed
10-20 seconds: Platforms get narrower, speed increases 20%
20-40 seconds: Moving platforms introduced, speed increases 40%
40-60 seconds: Hazards (spikes), speed increases 60%
60+ seconds: Maximum chaos, full speed
```

### 3. Polish ("Juice")
```
- Screen shake on collision
- Particle trails behind player
- Neon glow effects on everything
- Smooth camera following with slight lag
- Sound: Synth-wave background music, satisfying "dings" for pickups
- Visual: CRT screen effect, scanlines
```

## Art Style
**Visual Direction**: Retro neon aesthetic, cyberpunk, Tron-inspired
**Color Palette**: Hot pink (#FF006E), Electric blue (#00F5FF), Neon purple (#9D4EDD), Black (#000000)
**Style**: Pixel art with glow shaders, 64x64 sprites, simple geometric shapes
**References**: "Downwell" meets "Tron"

## Technical Scope
**Engine**: Pygame
**Resolution**: 800x600 (4:3 retro aspect ratio)
**Target Platform**: Windows/Mac/Linux desktop (itch.io)
**File Size Target**: Under 50MB
**Development Time**: 4 weeks

## Assets Needed
**Sprites**:
- Player character (4 frames idle, 4 frames falling)
- Platform (3 variations)
- Moving platform
- Hazards (spikes, lasers)
- Powerups (shield, slow-mo, magnet)
- Background elements (stars, grid)

**Audio**:
- Background music (synthwave, 2-3 minute loop)
- SFX: Jump, land, pickup, death, UI clicks

**UI**:
- Main menu
- High score display
- Game over screen
- Pause menu

## Success Metrics
- Playtime average: 5+ minutes per session
- "One more run" factor: High (measure via restart rate)
- itch.io rating target: 4+ stars
- Downloads target: 500+ in first month

## Marketing Angle
"I made a falling game in a week with AI-generated code and assets. Here's the dev log 🧵"

Built-in viral hook: "Can you beat my high score of [X]?"
```

### How to Fill This Out

**Spend 2-3 hours**:
1. Play similar games for inspiration (Downwell, Doodle Jump, etc.)
2. Sketch rough ideas on paper
3. Fill out DESIGN.md with YOUR specific decisions
4. Don't overthink - you can iterate later

**What Makes a Good Design for Automation**:
- Clear, specific mechanics (not vague)
- Limited scope (not "Minecraft clone")
- Defined art style (easy to prompt DALL-E)
- Simple controls (easier to code)

---

## Step 2: Set Up Claude to Generate Code

**Human Time**: 1 hour setup, 3-5 hours iteration
**Automation Level**: 70% (Claude writes code, you review and fix)

### Install Code Generation Tools

```bash
cd ~/Personas/agents/jordanthejet/game_dev_tools/

# Create code generator
touch code_generator.py
```

### Create `code_generator.py`

```python
"""
Game Code Generator - Uses Claude to generate game code from design docs
"""

import os
import json
from pathlib import Path
from anthropic import Anthropic

class GameCodeGenerator:
    def __init__(self, design_file: str, output_dir: str):
        self.design_file = design_file
        self.output_dir = Path(output_dir)
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        # Load design document
        with open(design_file, 'r') as f:
            self.design_doc = f.read()

    def generate_game_architecture(self) -> dict:
        """Generate overall game architecture and file structure"""

        prompt = f"""Based on this game design document, create a complete game architecture for Pygame.

DESIGN DOCUMENT:
{self.design_doc}

OUTPUT REQUIREMENTS:
1. File structure (JSON format)
2. Class architecture
3. Module responsibilities
4. Data flow between components

Return ONLY valid JSON in this format:
{{
  "files": [
    {{
      "path": "main.py",
      "description": "Main game loop and initialization",
      "dependencies": ["game.py", "config.py"]
    }},
    ...
  ],
  "classes": [
    {{
      "name": "Player",
      "file": "entities/player.py",
      "responsibilities": ["Movement", "Collision", "Rendering"],
      "methods": ["update()", "draw()", "handle_input()"]
    }},
    ...
  ]
}}
"""

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text

        # Extract JSON from markdown code blocks if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        architecture = json.loads(response_text)

        # Save architecture
        arch_file = self.output_dir / "architecture.json"
        with open(arch_file, 'w') as f:
            json.dump(architecture, f, indent=2)

        print(f"✓ Architecture generated: {arch_file}")
        return architecture

    def generate_file_code(self, filename: str, description: str, dependencies: list = None) -> str:
        """Generate code for a specific file"""

        deps_context = ""
        if dependencies:
            deps_context = "\n\nDEPENDENCIES:\n"
            for dep in dependencies:
                dep_path = self.output_dir / dep
                if dep_path.exists():
                    with open(dep_path, 'r') as f:
                        deps_context += f"\n--- {dep} ---\n{f.read()}\n"

        prompt = f"""Generate complete, working Python code for this game file.

DESIGN DOCUMENT:
{self.design_doc}

FILE TO GENERATE: {filename}
PURPOSE: {description}
{deps_context}

REQUIREMENTS:
1. Complete, runnable code (not pseudocode)
2. Include all imports
3. Add docstrings and comments
4. Follow Pygame best practices
5. Match the design specifications exactly
6. Handle edge cases and errors
7. Use type hints where appropriate

Generate ONLY the Python code, no explanations.
"""

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )

        code = message.content[0].text

        # Clean up markdown code blocks
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()

        return code

    def generate_config(self) -> str:
        """Generate game configuration file"""

        prompt = f"""Based on this design document, create a complete config.py file with all game constants.

DESIGN DOCUMENT:
{self.design_doc}

Include:
- Screen dimensions
- Colors (as RGB tuples)
- Player physics constants
- Game difficulty settings
- File paths for assets
- Any other constants from the design

Return ONLY Python code.
"""

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        code = message.content[0].text

        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()

        return code

    def generate_full_game(self):
        """Generate complete game from design document"""

        print("🎮 Generating game architecture...")
        architecture = self.generate_game_architecture()

        print("\n📝 Generating config.py...")
        config_code = self.generate_config()
        config_path = self.output_dir / "config.py"
        config_path.write_text(config_code)
        print(f"✓ Created: {config_path}")

        print("\n🔨 Generating game files...")
        for file_info in architecture["files"]:
            filepath = self.output_dir / file_info["path"]
            filepath.parent.mkdir(parents=True, exist_ok=True)

            print(f"\n  Generating {file_info['path']}...")
            code = self.generate_file_code(
                file_info["path"],
                file_info["description"],
                file_info.get("dependencies", [])
            )

            filepath.write_text(code)
            print(f"  ✓ Created: {filepath}")

        print("\n✅ Game generation complete!")
        print(f"\n📂 Game location: {self.output_dir}")
        print("\n🚀 To run: python main.py")


class GameCodeFixer:
    """Uses Claude to fix bugs and iterate on game code"""

    def __init__(self, game_dir: str):
        self.game_dir = Path(game_dir)
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def fix_error(self, error_message: str, relevant_files: list = None):
        """Fix a specific error"""

        # Load relevant files
        context = ""
        if relevant_files:
            for file in relevant_files:
                filepath = self.game_dir / file
                if filepath.exists():
                    with open(filepath, 'r') as f:
                        context += f"\n--- {file} ---\n{f.read()}\n"

        prompt = f"""Fix this error in the game code.

ERROR:
{error_message}

CURRENT CODE:
{context}

TASK:
1. Identify the issue
2. Provide the COMPLETE fixed code for each file that needs changes
3. Explain what was wrong

Format your response as:
EXPLANATION: [brief explanation]

FILE: [filename]
```python
[complete fixed code]
```

FILE: [next filename if needed]
```python
[complete fixed code]
```
"""

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text
        print(f"\n🔧 Claude's Fix:\n{response}")

        return response

    def improve_game_feel(self, feedback: str):
        """Iterate on game feel based on playtesting feedback"""

        # Load main game files
        main_code = (self.game_dir / "main.py").read_text()
        config_code = (self.game_dir / "config.py").read_text()

        prompt = f"""Improve the game based on this playtesting feedback.

FEEDBACK:
{feedback}

CURRENT main.py:
{main_code}

CURRENT config.py:
{config_code}

Adjust physics, timing, difficulty, or other parameters to address the feedback.
Return the updated files.
"""

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text


# Usage example
if __name__ == "__main__":
    generator = GameCodeGenerator(
        design_file="games/game_04/DESIGN.md",
        output_dir="games/game_04/src"
    )

    generator.generate_full_game()
```

### How to Use

**Generate Initial Game**:
```bash
cd ~/Personas/agents/jordanthejet/

# Create game directory
mkdir -p games/game_04/src

# Run generator
python game_dev_tools/code_generator.py
```

**What This Does**:
1. Reads your DESIGN.md
2. Generates complete file structure
3. Writes all Python game files
4. Creates working Pygame game

**Expected Output**:
```
games/game_04/src/
├── main.py              # Main game loop
├── config.py            # All constants
├── game.py              # Game state manager
├── entities/
│   ├── player.py        # Player class
│   ├── platform.py      # Platform class
│   └── pickup.py        # Pickup items
├── systems/
│   ├── renderer.py      # Rendering system
│   ├── physics.py       # Physics/collision
│   └── input_handler.py # Input processing
└── ui/
    ├── menu.py          # Main menu
    └── hud.py           # In-game HUD
```

**Testing the Generated Code**:
```bash
cd games/game_04/src/
python main.py
```

**When It Breaks** (It will):
```python
from game_dev_tools.code_generator import GameCodeFixer

fixer = GameCodeFixer(game_dir="games/game_04/src")

# Copy/paste the error message
error = """
Traceback (most recent call last):
  File "main.py", line 15, in <module>
    from entities.player import Player
ImportError: No module named 'entities.player'
"""

fixer.fix_error(error, relevant_files=["main.py", "entities/player.py"])
```

**Iteration Loop**:
1. Run game
2. Find issues (crashes, bad feel, boring)
3. Use `GameCodeFixer` to fix errors
4. Use `improve_game_feel()` for playtesting feedback
5. Repeat until fun

**Human Time**:
- Initial generation: Automated (5 minutes)
- Testing: 30 minutes
- Fixing errors: 2-3 hours (you copy/paste errors, Claude fixes)
- Improving game feel: 2-3 hours (you playtest, Claude adjusts)

**Total**: ~5 hours vs ~40 hours coding from scratch

---

## Step 3: Set Up DALL-E/Suno for Assets

**Human Time**: 1 hour setup, 2-3 hours curation
**Automation Level**: 80% (AI generates, you pick best)

### Install Asset Generation Tools

```bash
cd ~/Personas/agents/jordanthejet/game_dev_tools/

pip install openai Pillow requests
```

### Create `asset_generator.py`

```python
"""
Asset Generator - Uses DALL-E for sprites, Suno for music
"""

import os
import json
import requests
from pathlib import Path
from openai import OpenAI
from PIL import Image
import time

class AssetGenerator:
    def __init__(self, design_file: str, output_dir: str):
        self.design_file = design_file
        self.output_dir = Path(output_dir)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Load design doc to extract art style
        with open(design_file, 'r') as f:
            self.design_doc = f.read()

        # Parse art style from design doc
        self.art_style = self._extract_art_style()

        # Create output directories
        (self.output_dir / "sprites").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "backgrounds").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "ui").mkdir(parents=True, exist_ok=True)

    def _extract_art_style(self) -> dict:
        """Extract art style info from design doc"""
        # Simple extraction - in production, use Claude to parse
        return {
            "visual_direction": "retro neon aesthetic, cyberpunk, Tron-inspired",
            "color_palette": "hot pink, electric blue, neon purple, black",
            "style": "pixel art with glow effects, 64x64 sprites, geometric shapes"
        }

    def generate_sprite(self, description: str, filename: str, size: str = "1024x1024") -> str:
        """Generate a single sprite using DALL-E"""

        # Build complete prompt with art style
        full_prompt = f"""{description}, {self.art_style['visual_direction']},
{self.art_style['color_palette']} colors, {self.art_style['style']},
transparent background, game asset, centered, clean edges"""

        print(f"  Generating: {description}...")

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=full_prompt,
                size=size,
                quality="standard",
                n=1
            )

            image_url = response.data[0].url

            # Download image
            img_data = requests.get(image_url).content
            output_path = self.output_dir / "sprites" / filename

            with open(output_path, 'wb') as f:
                f.write(img_data)

            print(f"  ✓ Saved: {output_path}")

            # Track cost (DALL-E 4 pricing)
            cost = 0.04  # $0.04 per image for standard quality
            print(f"  💰 Cost: ${cost}")

            return str(output_path)

        except Exception as e:
            print(f"  ✗ Error: {e}")
            return None

    def generate_all_sprites(self):
        """Generate all sprites needed for game"""

        # Define all needed sprites
        sprites = [
            # Player
            ("player character, neon silhouette, falling pose, cyberpunk", "player_idle.png"),
            ("player character, neon silhouette, arms out, motion blur", "player_falling.png"),
            ("player character, neon silhouette, impact effect, particles", "player_hit.png"),

            # Platforms
            ("floating platform, neon glowing edges, geometric", "platform_01.png"),
            ("floating platform, neon glowing edges, geometric, wider", "platform_02.png"),
            ("moving platform, neon glowing edges, geometric, with arrows", "platform_moving.png"),

            # Hazards
            ("neon spikes, dangerous, glowing red, geometric", "hazard_spikes.png"),
            ("laser beam, horizontal, glowing red, dangerous", "hazard_laser.png"),

            # Powerups
            ("shield powerup icon, glowing blue, circular, protective", "powerup_shield.png"),
            ("slow motion icon, glowing purple, clock symbol", "powerup_slowmo.png"),
            ("magnet icon, glowing pink, magnetic field effect", "powerup_magnet.png"),

            # Effects
            ("particle trail, neon glow, small", "particle_trail.png"),
            ("explosion effect, neon particles, burst", "effect_explosion.png"),

            # Background elements
            ("starfield, small neon dots, scattered", "bg_stars.png"),
            ("grid pattern, neon lines, cyberpunk", "bg_grid.png"),
        ]

        print(f"\n🎨 Generating {len(sprites)} sprites...\n")

        total_cost = 0
        successful = 0

        for description, filename in sprites:
            result = self.generate_sprite(description, filename)
            if result:
                successful += 1
                total_cost += 0.04
            time.sleep(1)  # Rate limiting

        print(f"\n✅ Generated {successful}/{len(sprites)} sprites")
        print(f"💰 Total cost: ${total_cost:.2f}")

        # Generate sprite sheet from individual sprites
        self._create_sprite_sheet()

    def _create_sprite_sheet(self):
        """Combine sprites into sprite sheet for easier loading"""
        # Implementation for combining images into sheet
        print("\n📦 Creating sprite sheet...")
        # (Code to combine images - omitted for brevity)

    def generate_music(self) -> str:
        """Generate background music using Suno (semi-manual for now)"""

        print("\n🎵 Music Generation (Semi-Manual)")
        print("\nSuno doesn't have an official API yet (as of Nov 2025).")
        print("Manual process:")
        print("\n1. Go to: https://suno.ai")
        print("2. Use this prompt:")
        print(f"\n   'Synthwave instrumental, cyberpunk, retro 80s, Tron soundtrack style,")
        print(f"    upbeat tempo, looping, no vocals, electronic, neon aesthetic'")
        print("\n3. Generate 2-3 variations")
        print("4. Download best one as 'background_music.mp3'")
        print(f"5. Save to: {self.output_dir / 'audio' / 'background_music.mp3'}")
        print("\n⏱️ Estimated time: 10 minutes")
        print("💰 Cost: Free tier or $10/mo for Suno Pro")

        # Create audio directory
        (self.output_dir / "audio").mkdir(parents=True, exist_ok=True)

        return "Manual process - see instructions above"

    def generate_sfx(self):
        """Generate sound effects"""

        print("\n🔊 Sound Effects Generation")
        print("\nOptions:")
        print("\n1. ElevenLabs Sound Effects (Recommended)")
        print("   - Go to: https://elevenlabs.io/sound-effects")
        print("   - Generate:")
        print("     • 'retro video game jump sound, 8-bit'")
        print("     • 'retro video game land sound, impact'")
        print("     • 'retro video game pickup sound, coin, ding'")
        print("     • 'retro video game death sound, game over'")
        print("     • 'UI click sound, button press, digital'")
        print("\n2. Free Alternative: Freesound.org")
        print("   - Search for '8-bit jump', 'retro pickup', etc.")
        print("   - Filter by Creative Commons license")
        print("\n3. Generate with AI (via Stability Audio)")
        print("   - API available but requires separate integration")

        print(f"\n💾 Save all SFX to: {self.output_dir / 'audio' / 'sfx/'}")

        # Create sfx directory
        (self.output_dir / "audio" / "sfx").mkdir(parents=True, exist_ok=True)


# Post-processing utilities
class SpriteProcessor:
    """Post-process generated sprites"""

    @staticmethod
    def remove_background(image_path: str):
        """Remove background and make transparent"""
        from rembg import remove

        with open(image_path, 'rb') as f:
            input_img = f.read()

        output_img = remove(input_img)

        with open(image_path, 'wb') as f:
            f.write(output_img)

        print(f"  ✓ Background removed: {image_path}")

    @staticmethod
    def resize_sprite(image_path: str, target_size: tuple):
        """Resize sprite to target dimensions"""
        img = Image.open(image_path)
        img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
        img_resized.save(image_path)

        print(f"  ✓ Resized to {target_size}: {image_path}")

    @staticmethod
    def add_glow_effect(image_path: str, glow_color: tuple = (0, 245, 255)):
        """Add neon glow effect to sprite"""
        from PIL import ImageFilter, ImageEnhance

        img = Image.open(image_path).convert("RGBA")

        # Create glow layer
        glow = img.copy()
        glow = glow.filter(ImageFilter.GaussianBlur(radius=10))

        # Enhance brightness
        enhancer = ImageEnhance.Brightness(glow)
        glow = enhancer.enhance(2.0)

        # Composite glow behind original
        result = Image.alpha_composite(glow, img)
        result.save(image_path)

        print(f"  ✓ Glow added: {image_path}")


# Usage
if __name__ == "__main__":
    generator = AssetGenerator(
        design_file="games/game_04/DESIGN.md",
        output_dir="games/game_04/assets"
    )

    # Generate all sprites
    generator.generate_all_sprites()

    # Generate music (manual for now)
    generator.generate_music()

    # Generate SFX (manual for now)
    generator.generate_sfx()

    # Post-process sprites
    sprite_dir = Path("games/game_04/assets/sprites")
    for sprite in sprite_dir.glob("*.png"):
        SpriteProcessor.resize_sprite(str(sprite), (64, 64))
        SpriteProcessor.add_glow_effect(str(sprite))
```

### How to Use

**Generate All Assets**:
```bash
cd ~/Personas/agents/jordanthejet/

python game_dev_tools/asset_generator.py
```

**What This Does**:
1. Reads DESIGN.md art style
2. Generates all sprites via DALL-E (~$0.60 total)
3. Provides instructions for music/SFX
4. Post-processes for game-ready format

**Expected Output**:
```
games/game_04/assets/
├── sprites/
│   ├── player_idle.png
│   ├── player_falling.png
│   ├── platform_01.png
│   ├── hazard_spikes.png
│   └── ... (15+ sprites)
├── audio/
│   ├── background_music.mp3  (manual)
│   └── sfx/
│       ├── jump.wav  (manual)
│       ├── pickup.wav
│       └── death.wav
└── ui/
    └── ... (UI elements)
```

**Manual Steps** (20 minutes):
1. Go to Suno.ai, generate music (10 min)
2. Go to ElevenLabs, generate 5 SFX (10 min)
3. Download and save to correct folders

**Cost Breakdown**:
- Sprites: $0.60 (15 images × $0.04)
- Music: Free (Suno free tier) or $10/mo
- SFX: Free (ElevenLabs free tier) or $5/mo

**Human Time**:
- Setup script: 30 min
- Run generation: 5 min (automated)
- Manual music/SFX: 20 min
- Review and pick best: 1 hour
- Post-processing tweaks: 30 min

**Total**: ~2.5 hours vs ~20 hours creating art manually

---

## Step 4: Build Git Hooks to Track Progress

**Human Time**: 30 minutes setup
**Automation Level**: 95% (Fully automated tracking)

### Why Git Hooks?

Every time you commit code, the system:
1. Logs what changed
2. Tracks development velocity
3. Generates content for dev logs
4. Monitors progress toward milestones

**Zero manual tracking required.**

### Setup Git Hooks

```bash
cd ~/Personas/agents/jordanthejet/games/game_04/

# Initialize git if not already
git init

# Create hooks directory
mkdir -p .git/hooks/

# Create post-commit hook
touch .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

### Create Post-Commit Hook

Edit `.git/hooks/post-commit`:

```bash
#!/bin/bash

# Post-commit hook - tracks development progress
# Runs after every git commit

# Activate virtual environment
source ~/Personas/venv/bin/activate

# Run commit tracker
python ~/Personas/agents/jordanthejet/game_dev_tools/commit_tracker.py

# Exit with success
exit 0
```

### Create `commit_tracker.py`

```python
"""
Commit Tracker - Logs development activity for automated dev logs
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class CommitTracker:
    def __init__(self, game_dir: str = None):
        # Auto-detect game directory from git repo
        if game_dir is None:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True
            )
            game_dir = result.stdout.strip()

        self.game_dir = Path(game_dir)
        self.log_file = self.game_dir / "dev_log.json"

        # Load or create log
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                self.log = json.load(f)
        else:
            self.log = {
                "game": "game_04",
                "started": datetime.now().isoformat(),
                "commits": [],
                "sessions": [],
                "milestones": []
            }

    def get_last_commit_info(self) -> dict:
        """Get information about the last commit"""

        # Get commit hash
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H"],
            capture_output=True,
            text=True,
            cwd=self.game_dir
        )
        commit_hash = result.stdout.strip()

        # Get commit message
        result = subprocess.run(
            ["git", "log", "-1", "--format=%B"],
            capture_output=True,
            text=True,
            cwd=self.game_dir
        )
        commit_message = result.stdout.strip()

        # Get files changed
        result = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash],
            capture_output=True,
            text=True,
            cwd=self.game_dir
        )
        files_changed = result.stdout.strip().split('\n')

        # Get stats (insertions/deletions)
        result = subprocess.run(
            ["git", "log", "-1", "--stat", "--format="],
            capture_output=True,
            text=True,
            cwd=self.game_dir
        )
        stats = result.stdout.strip()

        return {
            "hash": commit_hash,
            "message": commit_message,
            "timestamp": datetime.now().isoformat(),
            "files_changed": files_changed,
            "stats": stats
        }

    def categorize_commit(self, commit_info: dict) -> str:
        """Categorize commit type based on files and message"""

        files = commit_info["files_changed"]
        message = commit_info["message"].lower()

        # Categorize
        if any("test" in f for f in files) or "test" in message:
            return "testing"
        elif any("asset" in f or "sprite" in f for f in files):
            return "art"
        elif "bug" in message or "fix" in message:
            return "bugfix"
        elif "polish" in message or "juice" in message:
            return "polish"
        elif any(".py" in f for f in files):
            return "code"
        else:
            return "other"

    def check_milestones(self, commit_info: dict):
        """Check if this commit triggers any milestones"""

        files = commit_info["files_changed"]

        milestones_to_check = [
            {
                "id": "first_commit",
                "name": "First Commit",
                "condition": lambda: len(self.log["commits"]) == 1
            },
            {
                "id": "player_movement",
                "name": "Player Movement Working",
                "condition": lambda: any("player.py" in f for f in files)
            },
            {
                "id": "first_playable",
                "name": "First Playable Build",
                "condition": lambda: "playable" in commit_info["message"].lower()
            },
            {
                "id": "all_mechanics",
                "name": "All Mechanics Implemented",
                "condition": lambda: "mechanics complete" in commit_info["message"].lower()
            },
            {
                "id": "final_polish",
                "name": "Final Polish Complete",
                "condition": lambda: "polish complete" in commit_info["message"].lower()
            },
        ]

        for milestone in milestones_to_check:
            # Check if already achieved
            if any(m["id"] == milestone["id"] for m in self.log["milestones"]):
                continue

            # Check condition
            if milestone["condition"]():
                self.log["milestones"].append({
                    "id": milestone["id"],
                    "name": milestone["name"],
                    "achieved_at": datetime.now().isoformat(),
                    "commit": commit_info["hash"]
                })
                print(f"🎉 Milestone achieved: {milestone['name']}")

    def track_commit(self):
        """Track the latest commit"""

        commit_info = self.get_last_commit_info()

        # Categorize
        commit_info["category"] = self.categorize_commit(commit_info)

        # Add to log
        self.log["commits"].append(commit_info)

        # Check milestones
        self.check_milestones(commit_info)

        # Save log
        with open(self.log_file, 'w') as f:
            json.dump(self.log, f, indent=2)

        print(f"✓ Tracked commit: {commit_info['message'][:50]}")
        print(f"  Category: {commit_info['category']}")
        print(f"  Files: {len(commit_info['files_changed'])}")

    def get_dev_summary(self, days: int = 7) -> dict:
        """Get development summary for last N days"""

        from datetime import timedelta

        cutoff = datetime.now() - timedelta(days=days)

        recent_commits = [
            c for c in self.log["commits"]
            if datetime.fromisoformat(c["timestamp"]) > cutoff
        ]

        # Categorize
        categories = {}
        for commit in recent_commits:
            cat = commit["category"]
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "total_commits": len(recent_commits),
            "categories": categories,
            "recent_milestones": [
                m for m in self.log["milestones"]
                if datetime.fromisoformat(m["achieved_at"]) > cutoff
            ]
        }


class SessionTracker:
    """Track development sessions (start/end of work)"""

    def __init__(self, game_dir: str):
        self.game_dir = Path(game_dir)
        self.tracker = CommitTracker(game_dir)

    def start_session(self):
        """Mark start of development session"""

        session = {
            "id": len(self.tracker.log["sessions"]) + 1,
            "started_at": datetime.now().isoformat(),
            "ended_at": None,
            "commits": 0,
            "focus": None  # Can set manually
        }

        self.tracker.log["sessions"].append(session)

        with open(self.tracker.log_file, 'w') as f:
            json.dump(self.tracker.log, f, indent=2)

        print(f"⏱️  Session started: #{session['id']}")

    def end_session(self, notes: str = ""):
        """Mark end of development session"""

        if not self.tracker.log["sessions"]:
            print("No active session")
            return

        session = self.tracker.log["sessions"][-1]

        if session["ended_at"] is not None:
            print("Session already ended")
            return

        session["ended_at"] = datetime.now().isoformat()
        session["notes"] = notes

        # Count commits during session
        start_time = datetime.fromisoformat(session["started_at"])
        session["commits"] = len([
            c for c in self.tracker.log["commits"]
            if datetime.fromisoformat(c["timestamp"]) > start_time
        ])

        with open(self.tracker.log_file, 'w') as f:
            json.dump(self.tracker.log, f, indent=2)

        duration = datetime.now() - start_time
        print(f"✓ Session ended: {duration} ({session['commits']} commits)")


class APIUsageTracker:
    """Track API usage costs for transparency"""

    def __init__(self, game_dir: str):
        self.game_dir = Path(game_dir)
        self.usage_file = self.game_dir / "api_usage.json"

        if self.usage_file.exists():
            with open(self.usage_file, 'r') as f:
                self.usage = json.load(f)
        else:
            self.usage = {
                "claude": {"calls": 0, "tokens": 0, "cost": 0},
                "dalle": {"calls": 0, "images": 0, "cost": 0},
                "suno": {"calls": 0, "songs": 0, "cost": 0}
            }

    def log_api_call(self, service: str, tokens: int = 0, cost: float = 0):
        """Log an API call"""

        if service not in self.usage:
            self.usage[service] = {"calls": 0, "tokens": 0, "cost": 0}

        self.usage[service]["calls"] += 1
        self.usage[service]["tokens"] += tokens
        self.usage[service]["cost"] += cost

        with open(self.usage_file, 'w') as f:
            json.dump(self.usage, f, indent=2)

    def get_total_cost(self) -> float:
        """Get total cost across all services"""
        return sum(s["cost"] for s in self.usage.values())


# CLI for manual session tracking
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        # Default: track commit (called by git hook)
        tracker = CommitTracker()
        tracker.track_commit()
    else:
        command = sys.argv[1]

        if command == "start":
            session_tracker = SessionTracker(".")
            session_tracker.start_session()

        elif command == "end":
            notes = sys.argv[2] if len(sys.argv) > 2 else ""
            session_tracker = SessionTracker(".")
            session_tracker.end_session(notes)

        elif command == "summary":
            tracker = CommitTracker()
            summary = tracker.get_dev_summary(days=7)
            print(json.dumps(summary, indent=2))
```

### How to Use

**Automatic Tracking** (Zero effort):
```bash
# Just commit as normal
git add .
git commit -m "Implemented player movement"

# Hook runs automatically and logs:
# - Commit message
# - Files changed
# - Category (code/art/bugfix/etc.)
# - Checks for milestones
```

**Manual Session Tracking** (Optional):
```bash
# Start work session
python game_dev_tools/commit_tracker.py start

# ... work for 2 hours, make commits ...

# End session
python game_dev_tools/commit_tracker.py end "Implemented jump physics, feels good"

# View summary
python game_dev_tools/commit_tracker.py summary
```

**What Gets Tracked**:

`dev_log.json`:
```json
{
  "game": "game_04",
  "started": "2025-11-20T09:00:00",
  "commits": [
    {
      "hash": "a3f8d9c",
      "message": "Implemented player movement",
      "timestamp": "2025-11-20T10:30:00",
      "files_changed": ["entities/player.py", "config.py"],
      "category": "code"
    },
    {
      "hash": "b7e2c1f",
      "message": "Added neon glow shader",
      "timestamp": "2025-11-20T14:15:00",
      "files_changed": ["systems/renderer.py"],
      "category": "polish"
    }
  ],
  "milestones": [
    {
      "id": "player_movement",
      "name": "Player Movement Working",
      "achieved_at": "2025-11-20T10:30:00",
      "commit": "a3f8d9c"
    }
  ],
  "sessions": [
    {
      "id": 1,
      "started_at": "2025-11-20T09:00:00",
      "ended_at": "2025-11-20T12:00:00",
      "commits": 3,
      "notes": "Good progress on movement"
    }
  ]
}
```

**Benefits**:
- Zero manual tracking
- Perfect memory of development
- Ready-made content for dev logs
- Shows real development velocity
- Transparency for followers

**Human Time**: 0 minutes (after 30 min setup)

---

## Step 5: Auto-Generate Dev Logs

**Human Time**: 15 minutes/week review
**Automation Level**: 90% (Automated generation, human approval)

### Create `devlog_generator.py`

```python
"""
Dev Log Generator - Creates dev log posts from commit history
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from anthropic import Anthropic
import tweepy

class DevLogGenerator:
    def __init__(self, game_dir: str):
        self.game_dir = Path(game_dir)
        self.dev_log_file = self.game_dir / "dev_log.json"
        self.claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        # Load dev log
        with open(self.dev_log_file, 'r') as f:
            self.dev_log = json.load(f)

    def generate_daily_devlog(self) -> str:
        """Generate a dev log tweet from today's activity"""

        # Get today's commits
        today = datetime.now().date()
        today_commits = [
            c for c in self.dev_log["commits"]
            if datetime.fromisoformat(c["timestamp"]).date() == today
        ]

        if not today_commits:
            return None  # No activity today

        # Build context for Claude
        context = {
            "commits_today": len(today_commits),
            "commit_messages": [c["message"] for c in today_commits],
            "categories": list(set(c["category"] for c in today_commits)),
            "total_commits": len(self.dev_log["commits"]),
            "days_since_start": (
                datetime.now() - datetime.fromisoformat(self.dev_log["started"])
            ).days
        }

        prompt = f"""You are JordanTheJet, an indie game developer building games with AI assistance.

Today's development activity:
{json.dumps(context, indent=2)}

Write a dev log tweet about today's work.

VOICE:
- Casual, transparent about AI usage
- Show the process, not just results
- Honest about challenges
- Under 280 characters
- Include what you're building, what worked, what didn't

EXAMPLES:
- "Day 3 of Neon Descent: got player movement working with Claude's help. Jump feels floaty tho, need to tweak gravity tomorrow. The AI generated sprites look sick with the glow shader 🔥"
- "Spent 2 hours debugging collisions. Claude kept suggesting the same fix that didn't work. Finally figured it out myself - classic. But hey, that's game dev 🤷"
- "Milestone: first playable build! You can fall, dodge platforms, die. It's ugly but it WORKS. AI generated all the code in 20 mins, took me 3 hours to fix it lol"

Write ONE tweet based on today's activity:
"""

        message = self.claude.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        tweet = message.content[0].text.strip()

        # Remove quotes if Claude added them
        if tweet.startswith('"') and tweet.endswith('"'):
            tweet = tweet[1:-1]

        return tweet

    def generate_weekly_summary(self) -> str:
        """Generate a weekly dev log thread"""

        # Get this week's activity
        week_ago = datetime.now() - timedelta(days=7)
        week_commits = [
            c for c in self.dev_log["commits"]
            if datetime.fromisoformat(c["timestamp"]) > week_ago
        ]

        # Get milestones
        week_milestones = [
            m for m in self.dev_log["milestones"]
            if datetime.fromisoformat(m["achieved_at"]) > week_ago
        ]

        context = {
            "commits_this_week": len(week_commits),
            "milestones": [m["name"] for m in week_milestones],
            "categories": {},
            "sessions": len([
                s for s in self.dev_log["sessions"]
                if datetime.fromisoformat(s["started_at"]) > week_ago
            ])
        }

        # Count categories
        for commit in week_commits:
            cat = commit["category"]
            context["categories"][cat] = context["categories"].get(cat, 0) + 1

        prompt = f"""You are JordanTheJet, indie game developer.

Write a weekly dev log THREAD (5-7 tweets) about this week's progress on "Neon Descent".

THIS WEEK'S STATS:
{json.dumps(context, indent=2)}

THREAD STRUCTURE:
1/ Hook - What you accomplished this week
2/ What you built (technical details)
3/ What went well (wins)
4/ What was hard (struggles)
5/ What you learned
6/ Next week's goals
7/ Call to action (follow for updates)

VOICE:
- Transparent about using AI tools
- Show the real process (messy, iterative)
- Educational (teach others)
- Humble but proud of progress

Write the thread in this format:
1/ [tweet]

2/ [tweet]

...etc
"""

        message = self.claude.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        thread = message.content[0].text.strip()

        return thread

    def generate_milestone_post(self, milestone_id: str) -> str:
        """Generate a post for achieving a milestone"""

        # Find milestone
        milestone = next(
            (m for m in self.dev_log["milestones"] if m["id"] == milestone_id),
            None
        )

        if not milestone:
            return None

        prompt = f"""You achieved a milestone: {milestone['name']}

Write an excited tweet about hitting this milestone.

TONE: Genuinely excited, share the win
LENGTH: Under 280 characters
INCLUDE: What the milestone means, quick screenshot/gif callout

Example:
"🎉 FIRST PLAYABLE BUILD! You can actually play Neon Descent now. It's rough but you can fall, dodge platforms, and die spectacularly. Check the vid 👇"

Write ONE tweet:
"""

        message = self.claude.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        tweet = message.content[0].text.strip()

        if tweet.startswith('"'):
            tweet = tweet[1:-1]

        return tweet


class AutoScreenshot:
    """Automatically capture screenshots during development"""

    @staticmethod
    def capture_gameplay(game_window_title: str, output_path: str):
        """Capture screenshot of game window"""
        import pyautogui

        # Find game window and capture
        screenshot = pyautogui.screenshot()
        screenshot.save(output_path)

        print(f"📸 Screenshot saved: {output_path}")


class DevLogPoster:
    """Post dev logs to Twitter"""

    def __init__(self):
        self.twitter = tweepy.Client(
            consumer_key=os.getenv("JORDAN_TWITTER_API_KEY"),
            consumer_secret=os.getenv("JORDAN_TWITTER_API_SECRET"),
            access_token=os.getenv("JORDAN_TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("JORDAN_TWITTER_ACCESS_SECRET")
        )

    def post_tweet(self, text: str, image_path: str = None) -> str:
        """Post a tweet, optionally with image"""

        # For now, just approve and post manually
        # In production, add human-in-the-loop approval

        print("\n" + "="*60)
        print("DRAFT TWEET:")
        print("="*60)
        print(text)
        if image_path:
            print(f"\nImage: {image_path}")
        print("="*60)

        approval = input("\nPost this tweet? (y/n): ")

        if approval.lower() == 'y':
            response = self.twitter.create_tweet(text=text)
            tweet_id = response.data['id']
            print(f"\n✓ Posted: https://twitter.com/user/status/{tweet_id}")
            return tweet_id
        else:
            print("\n✗ Tweet not posted")
            return None

    def post_thread(self, thread_text: str):
        """Post a Twitter thread"""

        # Split thread into individual tweets
        tweets = []
        for line in thread_text.split('\n'):
            if line.strip() and line[0].isdigit() and '/' in line[:3]:
                tweet = line.split('/', 1)[1].strip()
                tweets.append(tweet)

        print("\n" + "="*60)
        print(f"DRAFT THREAD ({len(tweets)} tweets):")
        print("="*60)
        for i, tweet in enumerate(tweets, 1):
            print(f"\n{i}/ {tweet}")
        print("="*60)

        approval = input("\nPost this thread? (y/n): ")

        if approval.lower() == 'y':
            previous_tweet_id = None

            for i, tweet in enumerate(tweets, 1):
                if previous_tweet_id:
                    response = self.twitter.create_tweet(
                        text=tweet,
                        in_reply_to_tweet_id=previous_tweet_id
                    )
                else:
                    response = self.twitter.create_tweet(text=tweet)

                previous_tweet_id = response.data['id']
                print(f"✓ Posted tweet {i}/{len(tweets)}")

            print(f"\n✓ Thread posted: https://twitter.com/user/status/{previous_tweet_id}")
        else:
            print("\n✗ Thread not posted")


# Daily automation
if __name__ == "__main__":
    import sys

    generator = DevLogGenerator("games/game_04")
    poster = DevLogPoster()

    if len(sys.argv) > 1 and sys.argv[1] == "weekly":
        # Weekly summary thread
        thread = generator.generate_weekly_summary()
        poster.post_thread(thread)
    else:
        # Daily dev log
        tweet = generator.generate_daily_devlog()
        if tweet:
            poster.post_tweet(tweet)
        else:
            print("No activity today, skipping dev log")
```

### How to Use

**Daily Dev Logs** (Automated):
```bash
# Add to crontab to run every evening at 6pm
0 18 * * * cd ~/Personas/agents/jordanthejet && python game_dev_tools/devlog_generator.py
```

**Weekly Summaries** (Semi-automated):
```bash
# Run manually every Sunday
python game_dev_tools/devlog_generator.py weekly
```

**What This Generates**:

Daily tweet example:
```
Day 5 of Neon Descent: collision detection working! Claude generated
the physics code, took me an hour to integrate. Platform spawning is
still wonky but it's playable 🎮
```

Weekly thread example:
```
1/ Week 1 of building Neon Descent with AI: ✅ Player movement ✅
Platform generation ✅ Collision system ✅ First playable build

Not bad for ~15 hours of actual work

2/ Technical deep dive: Used Claude Sonnet 4.5 to generate ~80% of the
code. DALL-E 4 for all sprites ($0.60 total). Suno for music (free tier)

Total AI cost so far: ~$12

3/ What went well: The initial code generation was shockingly good.
Claude understood the design doc and created working architecture in
one shot.

4/ What was hard: The generated collision code had a bug that took
3 hours to find. Classic off-by-one error. AI can't catch everything.

5/ Biggest learning: AI is incredible for boilerplate and structure,
but game FEEL still needs human iteration. Jump physics took 50 tweaks
to feel right.

6/ Next week: Polish, juice, SFX integration, first public demo

7/ Building in public. Follow along if you want to see how indie games
get made with AI in 2025 🚀
```

**Human Time**:
- Review daily tweet: 1 min
- Review weekly thread: 5 min
- Edit if needed: 5 min
- Approve and post: 1 min

**Total per week**: 15 minutes vs 2+ hours writing from scratch

---

## Step 6: Auto-Create Videos

**Human Time**: 1 hour setup, 30 min/week review
**Automation Level**: 85% (Automated creation, human approval)

### Why Video?

Video content gets **10x more engagement** than text:
- YouTube dev logs build audience
- Twitter videos go viral
- itch.io trailer drives downloads
- Reusable across platforms

### Video Types to Automate

1. **Dev Log Videos** (Weekly, 2-5 min)
2. **Feature Showcase** (As needed, 30-60 sec)
3. **Game Trailer** (Final release, 60-90 sec)
4. **Gameplay Clips** (Daily, 10-30 sec)

### Install Video Tools

```bash
pip install moviepy pyautogui pillow anthropic elevenlabs
```

### Create `video_generator.py`

```python
"""
Video Generator - Automated dev log and gameplay video creation
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from anthropic import Anthropic
from elevenlabs import ElevenLabs, Voice
from moviepy.editor import *
import subprocess

class DevLogVideoGenerator:
    def __init__(self, game_dir: str):
        self.game_dir = Path(game_dir)
        self.dev_log_file = self.game_dir / "dev_log.json"
        self.screenshots_dir = self.game_dir / "screenshots"
        self.videos_dir = self.game_dir / "videos"

        self.claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

        # Load dev log
        with open(self.dev_log_file, 'r') as f:
            self.dev_log = json.load(f)

        # Ensure directories exist
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.videos_dir.mkdir(parents=True, exist_ok=True)

    def generate_script(self, duration_seconds: int = 180) -> dict:
        """Generate video script from week's activity"""

        # Get this week's activity
        week_ago = datetime.now() - timedelta(days=7)
        week_commits = [
            c for c in self.dev_log["commits"]
            if datetime.fromisoformat(c["timestamp"]) > week_ago
        ]

        week_milestones = [
            m for m in self.dev_log["milestones"]
            if datetime.fromisoformat(m["achieved_at"]) > week_ago
        ]

        context = {
            "week_number": (datetime.now() - datetime.fromisoformat(self.dev_log["started"])).days // 7 + 1,
            "commits": len(week_commits),
            "milestones": [m["name"] for m in week_milestones],
            "key_work": [c["message"] for c in week_commits[:5]]  # Top 5 commits
        }

        prompt = f"""Generate a script for a {duration_seconds}-second dev log video.

CONTEXT:
{json.dumps(context, indent=2)}

STRUCTURE:
- Hook (0-10s): Grab attention
- Progress (10-120s): What you built this week
- Demo (120-150s): Show it working
- Learnings (150-170s): What you learned
- CTA (170-180s): Next week + subscribe

TONE: JordanTheJet voice
- Casual, conversational (like talking to a friend)
- Transparent about AI usage
- Educational (share learnings)
- Authentic (honest about struggles)

OUTPUT FORMAT (JSON):
{{
  "title": "Week X Dev Log: [Title]",
  "script": [
    {{
      "timestamp": "0:00",
      "duration_seconds": 10,
      "narration": "What's up, Jordan here...",
      "visual": "Title card with game logo"
    }},
    ...
  ],
  "total_duration": 180
}}
"""

        message = self.claude.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text

        # Extract JSON
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()

        script = json.loads(response_text)

        # Save script
        script_file = self.videos_dir / f"script_week_{context['week_number']}.json"
        with open(script_file, 'w') as f:
            json.dump(script, f, indent=2)

        print(f"✓ Script generated: {script_file}")

        return script

    def generate_voiceover(self, script: dict) -> str:
        """Generate voiceover from script using ElevenLabs"""

        # Combine all narration
        full_narration = "\n\n".join([
            segment["narration"] for segment in script["script"]
        ])

        print(f"🎙️ Generating voiceover ({len(full_narration)} chars)...")

        # Generate with ElevenLabs
        audio = self.elevenlabs.text_to_speech.convert(
            text=full_narration,
            voice=Voice(
                voice_id="21m00Tcm4TlvDq8ikWAM",  # "Rachel" - or pick your own
                name="Jordan Voice"
            ),
            model_id="eleven_multilingual_v2"
        )

        # Save audio
        audio_file = self.videos_dir / f"voiceover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        with open(audio_file, 'wb') as f:
            for chunk in audio:
                f.write(chunk)

        print(f"✓ Voiceover saved: {audio_file}")

        return str(audio_file)

    def collect_visuals(self, script: dict) -> list:
        """Collect or generate visuals for each script segment"""

        visuals = []

        for i, segment in enumerate(script["script"]):
            visual_desc = segment["visual"]

            # Determine visual type
            if "title card" in visual_desc.lower():
                # Generate title card
                visual_path = self._generate_title_card(script["title"])

            elif "gameplay" in visual_desc.lower() or "demo" in visual_desc.lower():
                # Use gameplay recording
                visual_path = self._get_gameplay_clip(segment["duration_seconds"])

            elif "screenshot" in visual_desc.lower() or "code" in visual_desc.lower():
                # Use screenshot
                visual_path = self._get_relevant_screenshot(segment["timestamp"])

            else:
                # Default: use game screenshot
                visual_path = self._get_latest_screenshot()

            visuals.append({
                "segment": i,
                "path": visual_path,
                "duration": segment["duration_seconds"]
            })

        return visuals

    def _generate_title_card(self, title: str) -> str:
        """Generate title card image"""
        from PIL import Image, ImageDraw, ImageFont

        # Create image
        img = Image.new('RGB', (1920, 1080), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Add text (simplified - in production, use better fonts)
        font_size = 72
        text = title

        # Calculate position (centered)
        bbox = draw.textbbox((0, 0), text, font=None)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((1920 - text_width) // 2, (1080 - text_height) // 2)

        draw.text(position, text, fill=(255, 255, 255))

        # Save
        output_path = self.videos_dir / "title_card.png"
        img.save(output_path)

        return str(output_path)

    def _get_gameplay_clip(self, duration: int) -> str:
        """Get gameplay footage (recorded separately)"""
        # In production, use OBS or similar to auto-record
        # For now, assume clips exist in screenshots/gameplay/

        gameplay_dir = self.screenshots_dir / "gameplay"
        if gameplay_dir.exists():
            clips = list(gameplay_dir.glob("*.mp4"))
            if clips:
                return str(clips[-1])  # Latest clip

        # Fallback: use screenshot
        return self._get_latest_screenshot()

    def _get_relevant_screenshot(self, timestamp: str) -> str:
        """Get screenshot relevant to this part of video"""
        # Simple: just use latest screenshot
        # In production: match screenshots to commit timestamps
        return self._get_latest_screenshot()

    def _get_latest_screenshot(self) -> str:
        """Get most recent screenshot"""
        screenshots = list(self.screenshots_dir.glob("*.png"))
        if screenshots:
            return str(sorted(screenshots)[-1])
        else:
            # Generate placeholder
            return self._generate_placeholder()

    def _generate_placeholder(self) -> str:
        """Generate placeholder image"""
        from PIL import Image
        img = Image.new('RGB', (1920, 1080), color=(20, 20, 20))
        output_path = self.screenshots_dir / "placeholder.png"
        img.save(output_path)
        return str(output_path)

    def create_video(self, script: dict, voiceover_path: str, visuals: list) -> str:
        """Combine voiceover and visuals into final video"""

        print("🎬 Creating video...")

        # Load voiceover
        audio = AudioFileClip(voiceover_path)

        # Create video clips for each segment
        clips = []

        for visual in visuals:
            # Load image or video
            if visual["path"].endswith(('.mp4', '.mov')):
                clip = VideoFileClip(visual["path"])
            else:
                clip = ImageClip(visual["path"])

            # Set duration
            clip = clip.set_duration(visual["duration"])

            clips.append(clip)

        # Concatenate clips
        final_video = concatenate_videoclips(clips, method="compose")

        # Add voiceover
        final_video = final_video.set_audio(audio)

        # Add background music (if available)
        music_path = self.game_dir / "assets" / "audio" / "background_music.mp3"
        if music_path.exists():
            music = AudioFileClip(str(music_path))
            music = music.volumex(0.2)  # Lower volume (background)
            music = music.set_duration(final_video.duration)

            # Mix audio
            final_audio = CompositeAudioClip([final_video.audio, music])
            final_video = final_video.set_audio(final_audio)

        # Export
        output_path = self.videos_dir / f"devlog_{datetime.now().strftime('%Y%m%d')}.mp4"
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )

        print(f"✅ Video created: {output_path}")
        print(f"📊 Duration: {final_video.duration}s")

        return str(output_path)

    def generate_full_devlog_video(self) -> str:
        """Full pipeline: script → voiceover → visuals → video"""

        print("\n🎥 Generating Dev Log Video\n")

        # 1. Generate script
        print("Step 1: Generating script...")
        script = self.generate_script(duration_seconds=180)

        # 2. Generate voiceover
        print("\nStep 2: Generating voiceover...")
        voiceover_path = self.generate_voiceover(script)

        # 3. Collect visuals
        print("\nStep 3: Collecting visuals...")
        visuals = self.collect_visuals(script)

        # 4. Create video
        print("\nStep 4: Creating video...")
        video_path = self.create_video(script, voiceover_path, visuals)

        print("\n✅ Dev log video complete!")
        print(f"📹 Video: {video_path}")

        return video_path


class GameplayRecorder:
    """Auto-record gameplay footage"""

    def __init__(self, game_dir: str):
        self.game_dir = Path(game_dir)
        self.recordings_dir = self.game_dir / "screenshots" / "gameplay"
        self.recordings_dir.mkdir(parents=True, exist_ok=True)

    def start_recording(self):
        """Start recording gameplay (uses OBS or similar)"""

        # Option 1: OBS Studio via obs-websocket
        # Option 2: FFmpeg screen capture
        # Option 3: Python screen recording

        # Using FFmpeg (cross-platform):
        output_file = self.recordings_dir / f"gameplay_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

        # Linux/Mac
        if os.name != 'nt':
            command = [
                'ffmpeg',
                '-f', 'x11grab',
                '-framerate', '30',
                '-video_size', '800x600',
                '-i', ':0.0+100,200',  # Adjust based on game window position
                '-t', '30',  # Record for 30 seconds
                '-c:v', 'libx264',
                str(output_file)
            ]
        # Windows
        else:
            command = [
                'ffmpeg',
                '-f', 'gdigrab',
                '-framerate', '30',
                '-i', 'desktop',
                '-t', '30',
                str(output_file)
            ]

        print(f"🎥 Recording gameplay for 30 seconds...")
        subprocess.run(command, capture_output=True)
        print(f"✓ Recording saved: {output_file}")

        return str(output_file)


class VideoUploader:
    """Upload videos to platforms"""

    def upload_to_youtube(self, video_path: str, title: str, description: str):
        """Upload to YouTube (requires setup)"""

        # Uses youtube-upload library or YouTube Data API
        # Requires OAuth authentication

        print(f"\n📤 YouTube Upload (Manual for now)")
        print(f"Video: {video_path}")
        print(f"Title: {title}")
        print(f"Description: {description}")
        print("\nGo to: https://studio.youtube.com/")
        print("Upload manually and optimize:")
        print("- Thumbnail: Create with Canva")
        print("- Tags: indie game dev, AI game development, devlog")
        print("- Category: Gaming")

    def post_to_twitter(self, video_path: str, caption: str):
        """Upload video to Twitter"""

        # Twitter API v2 supports video upload
        # Requires media upload endpoint

        print(f"\n📤 Twitter Video Upload")
        print(f"Video: {video_path}")
        print(f"Caption: {caption}")
        print("\nUpload via Twitter web interface for now")


# Usage
if __name__ == "__main__":
    generator = DevLogVideoGenerator("games/game_04")

    # Generate full dev log video
    video_path = generator.generate_full_devlog_video()

    # Upload (manual approval)
    uploader = VideoUploader()
    uploader.upload_to_youtube(
        video_path,
        title="Week 1: Building Neon Descent with AI",
        description="Building an indie game with AI assistance. Full transparency."
    )
```

### How to Use

**Weekly Dev Log Video** (Semi-automated):
```bash
# Run every Sunday
python game_dev_tools/video_generator.py
```

**What This Does**:
1. Reads dev_log.json (your week's activity)
2. Generates 3-minute video script
3. Creates voiceover with ElevenLabs
4. Combines with screenshots/gameplay
5. Exports finished video
6. Prompts for upload approval

**Expected Output**:
```
videos/
├── script_week_1.json
├── voiceover_20251120.mp3
└── devlog_20251120.mp4  (3 min, ready to upload)
```

**Manual Steps** (30 minutes):
1. Review script (5 min)
2. Record 30 seconds of gameplay (5 min)
3. Review generated video (5 min)
4. Create thumbnail in Canva (10 min)
5. Upload to YouTube + Twitter (5 min)

**Cost**:
- ElevenLabs voiceover: $0.30 per video (or free tier)
- Video processing: $0 (local)
- Total: ~$1.20/month for weekly videos

**Human Time**: 30 min/week vs 4+ hours editing from scratch

---

## Step 7: Auto-Market Everything

**Human Time**: 1 hour setup, 15 min/day review
**Automation Level**: 85% (Automated posting, human approval)

### Marketing Channels

**For Game Launch**:
1. Twitter/X (JordanTheJet account)
2. Reddit (r/gamedev, r/indiegames, r/playmygame)
3. itch.io (game page + devlog)
4. YouTube (dev log videos)
5. Discord (gamedev communities)
6. Newsletter (build email list)

### Create `marketing_automation.py`

```python
"""
Marketing Automation - Multi-platform distribution
"""

import os
import json
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic
import tweepy
import praw  # Reddit API

class MarketingCampaign:
    def __init__(self, game_dir: str):
        self.game_dir = Path(game_dir)
        self.campaign_file = self.game_dir / "marketing_campaign.json"
        self.claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        # Load or create campaign
        if self.campaign_file.exists():
            with open(self.campaign_file, 'r') as f:
                self.campaign = json.load(f)
        else:
            self.campaign = {
                "game": "Neon Descent",
                "launch_date": None,
                "pre_launch_posts": [],
                "launch_posts": [],
                "post_launch_posts": []
            }

    def generate_launch_campaign(self, launch_date: str):
        """Generate complete marketing campaign for game launch"""

        # Load game info
        design_file = self.game_dir / "DESIGN.md"
        with open(design_file, 'r') as f:
            design_doc = f.read()

        prompt = f"""Create a complete marketing campaign for this indie game launch.

GAME INFO:
{design_doc}

LAUNCH DATE: {launch_date}

CAMPAIGN STRUCTURE:
1. Pre-launch (2 weeks before): Build hype
   - Teaser posts
   - Behind-the-scenes
   - Countdown
2. Launch day: Maximum visibility
   - Announcement posts
   - Trailer
   - Press outreach
3. Post-launch (2 weeks after): Sustain momentum
   - Player highlights
   - Update posts
   - Community engagement

For each post, specify:
- Platform (Twitter/Reddit/itch.io)
- Post date/time
- Content (text)
- Media (screenshot/video/gif)
- Hashtags/flair

VOICE: JordanTheJet
- Authentic, transparent about process
- Focus on the journey, not just the product
- Engage with community
- Educational (share learnings)

OUTPUT as JSON:
{{
  "pre_launch": [
    {{
      "date": "2025-12-01",
      "time": "10:00",
      "platform": "Twitter",
      "content": "...",
      "media": "teaser_gif",
      "hashtags": ["#indiegame", "#gamedev"]
    }},
    ...
  ],
  "launch": [...],
  "post_launch": [...]
}}
"""

        message = self.claude.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text

        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()

        campaign = json.loads(response)
        campaign["launch_date"] = launch_date

        # Save campaign
        self.campaign = campaign
        with open(self.campaign_file, 'w') as f:
            json.dump(campaign, f, indent=2)

        print(f"✓ Marketing campaign generated: {len(campaign['pre_launch']) + len(campaign['launch']) + len(campaign['post_launch'])} posts")

        return campaign

    def generate_platform_specific_post(self, base_content: str, platform: str) -> str:
        """Adapt content for specific platform"""

        prompt = f"""Adapt this post for {platform}.

ORIGINAL CONTENT:
{base_content}

PLATFORM: {platform}

PLATFORM GUIDELINES:
Twitter: 280 chars, casual, hashtags, emoji OK
Reddit: Longer OK, no hashtags, authentic tone, add context
itch.io: Very detailed, educational, dev perspective

Adapt the content while keeping the core message.
"""

        message = self.claude.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text.strip()


class MultiPlatformPoster:
    """Post to multiple platforms"""

    def __init__(self):
        # Twitter
        self.twitter = tweepy.Client(
            consumer_key=os.getenv("JORDAN_TWITTER_API_KEY"),
            consumer_secret=os.getenv("JORDAN_TWITTER_API_SECRET"),
            access_token=os.getenv("JORDAN_TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("JORDAN_TWITTER_ACCESS_SECRET")
        )

        # Reddit
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent="GameDevBot by u/YourUsername",
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD")
        )

    def post_to_twitter(self, content: str, media_path: str = None) -> str:
        """Post to Twitter"""

        print("\n--- TWITTER POST ---")
        print(content)
        if media_path:
            print(f"Media: {media_path}")

        approval = input("\nPost? (y/n): ")

        if approval.lower() == 'y':
            response = self.twitter.create_tweet(text=content)
            tweet_id = response.data['id']
            url = f"https://twitter.com/user/status/{tweet_id}"
            print(f"✓ Posted: {url}")
            return url
        else:
            print("✗ Skipped")
            return None

    def post_to_reddit(self, subreddit: str, title: str, content: str, flair: str = None):
        """Post to Reddit"""

        print(f"\n--- REDDIT POST (r/{subreddit}) ---")
        print(f"Title: {title}")
        print(f"Content:\n{content}")
        if flair:
            print(f"Flair: {flair}")

        approval = input("\nPost? (y/n): ")

        if approval.lower() == 'y':
            sub = self.reddit.subreddit(subreddit)
            submission = sub.submit(title, selftext=content, flair_id=flair)
            url = f"https://reddit.com{submission.permalink}"
            print(f"✓ Posted: {url}")
            return url
        else:
            print("✗ Skipped")
            return None

    def post_to_itchio_devlog(self, game_slug: str, title: str, content: str):
        """Post devlog to itch.io (manual for now)"""

        print(f"\n--- ITCH.IO DEVLOG ---")
        print(f"Game: {game_slug}")
        print(f"Title: {title}")
        print(f"Content:\n{content}")
        print(f"\nGo to: https://{game_slug}.itch.io/devlog")
        print("Post manually (itch.io has no official API)")


class ScheduledPoster:
    """Schedule posts for optimal times"""

    def __init__(self, campaign_file: str):
        with open(campaign_file, 'r') as f:
            self.campaign = json.load(f)

    def get_todays_posts(self) -> list:
        """Get posts scheduled for today"""

        today = datetime.now().date().isoformat()

        all_posts = (
            self.campaign.get("pre_launch", []) +
            self.campaign.get("launch", []) +
            self.campaign.get("post_launch", [])
        )

        todays_posts = [
            p for p in all_posts
            if p.get("date") == today
        ]

        return todays_posts

    def post_scheduled_content(self):
        """Post today's scheduled content"""

        todays_posts = self.get_todays_posts()

        if not todays_posts:
            print("No posts scheduled for today")
            return

        print(f"\n📅 {len(todays_posts)} posts scheduled for today\n")

        poster = MultiPlatformPoster()

        for post in todays_posts:
            platform = post["platform"]
            content = post["content"]

            if platform == "Twitter":
                poster.post_to_twitter(content, post.get("media"))

            elif platform == "Reddit":
                poster.post_to_reddit(
                    subreddit=post.get("subreddit", "indiegames"),
                    title=post.get("title", content[:100]),
                    content=content,
                    flair=post.get("flair")
                )

            elif platform == "itch.io":
                poster.post_to_itchio_devlog(
                    game_slug=post.get("game_slug", "neon-descent"),
                    title=post.get("title"),
                    content=content
                )


class AnalyticsTracker:
    """Track marketing performance"""

    def __init__(self, game_dir: str):
        self.game_dir = Path(game_dir)
        self.analytics_file = self.game_dir / "analytics.json"

        if self.analytics_file.exists():
            with open(self.analytics_file, 'r') as f:
                self.analytics = json.load(f)
        else:
            self.analytics = {
                "posts": [],
                "downloads": [],
                "engagement": {}
            }

    def track_post(self, platform: str, url: str, content: str):
        """Track a marketing post"""

        post_data = {
            "platform": platform,
            "url": url,
            "content": content[:100],
            "posted_at": datetime.now().isoformat(),
            "views": 0,
            "engagement": 0,
            "clicks": 0
        }

        self.analytics["posts"].append(post_data)
        self._save()

    def update_metrics(self, post_url: str, views: int, engagement: int, clicks: int):
        """Update metrics for a post"""

        for post in self.analytics["posts"]:
            if post["url"] == post_url:
                post["views"] = views
                post["engagement"] = engagement
                post["clicks"] = clicks
                break

        self._save()

    def _save(self):
        with open(self.analytics_file, 'w') as f:
            json.dump(self.analytics, f, indent=2)

    def get_performance_summary(self) -> dict:
        """Get marketing performance summary"""

        total_posts = len(self.analytics["posts"])
        total_views = sum(p["views"] for p in self.analytics["posts"])
        total_engagement = sum(p["engagement"] for p in self.analytics["posts"])

        return {
            "total_posts": total_posts,
            "total_views": total_views,
            "total_engagement": total_engagement,
            "avg_engagement_rate": total_engagement / total_views if total_views > 0 else 0
        }


# Usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        # Generate campaign
        campaign_gen = MarketingCampaign("games/game_04")
        campaign_gen.generate_launch_campaign("2025-12-15")

    elif len(sys.argv) > 1 and sys.argv[1] == "post":
        # Post scheduled content
        scheduler = ScheduledPoster("games/game_04/marketing_campaign.json")
        scheduler.post_scheduled_content()

    else:
        print("Usage:")
        print("  python marketing_automation.py generate  # Generate campaign")
        print("  python marketing_automation.py post      # Post today's content")
```

### How to Use

**Generate Marketing Campaign** (Once, before launch):
```bash
python game_dev_tools/marketing_automation.py generate
```

**Daily Posting** (Automated via cron):
```bash
# Add to crontab - runs daily at 9am
0 9 * * * cd ~/Personas/agents/jordanthejet && python game_dev_tools/marketing_automation.py post
```

**What This Generates**:

`marketing_campaign.json`:
```json
{
  "launch_date": "2025-12-15",
  "pre_launch": [
    {
      "date": "2025-12-01",
      "time": "10:00",
      "platform": "Twitter",
      "content": "Started something new. Neon aesthetic, falling mechanics, pure chaos. First playable build this week 🎮",
      "media": "teaser.gif",
      "hashtags": ["#indiegamedev", "#screenshotsaturday"]
    },
    ...
  ],
  "launch": [
    {
      "date": "2025-12-15",
      "time": "10:00",
      "platform": "Twitter",
      "content": "Neon Descent is LIVE ✨ Built in 6 weeks with AI assistance. Free to play on itch.io. Can you beat my high score? 🎯",
      "media": "trailer.mp4",
      "hashtags": ["#indiegame", "#gamedev", "#AIgamedev"]
    },
    {
      "date": "2025-12-15",
      "time": "12:00",
      "platform": "Reddit",
      "subreddit": "indiegames",
      "title": "I built a falling platformer with AI in 6 weeks - Neon Descent is live!",
      "content": "Full dev transparency: I used Claude for code gen, DALL-E for art, and learned a TON. Free to play, would love feedback...",
      "flair": "Game Release"
    }
  ],
  "post_launch": [...]
}
```

**Human Workflow**:
1. Wake up, check scheduled posts (5 min)
2. Approve or edit (5 min)
3. Monitor engagement (5 min)
4. Respond to comments (varies)

**Cost**: $0 (all free platforms)

**Time**: 15 min/day vs 2+ hours manual marketing

---

## Summary: Complete Automation Stack

### Human Time Breakdown

| Step | Setup | Ongoing/Week |
|------|-------|--------------|
| 1. Design Game | 0 min | 180 min (one-time) |
| 2. Code Generation | 60 min | 180-300 min (iteration) |
| 3. Asset Generation | 30 min | 90 min (curation) |
| 4. Git Tracking | 30 min | 0 min (automatic) |
| 5. Dev Logs | 0 min | 15 min (review) |
| 6. Videos | 60 min | 30 min (review) |
| 7. Marketing | 60 min | 105 min (7 days × 15 min) |
| **TOTAL** | **240 min** | **340-440 min/week** |

**5-7 hours/week** to ship a complete game with full marketing.

Compare to traditional: **30-40 hours/week**

**Time saved: 85%**

### Cost Breakdown

| Service | Monthly Cost |
|---------|--------------|
| Claude API (code gen) | $20-50 |
| OpenAI (DALL-E, GPT) | $10-30 |
| ElevenLabs (voice) | $0-11 |
| Suno (music) | $0-10 |
| **TOTAL** | **$30-101/month** |

**Per game** (4-6 weeks): **$60-200**

Traditional cost (hiring): **$5,000-20,000**

### What's Automated

✅ Code generation (70%)
✅ Asset creation (80%)
✅ Progress tracking (95%)
✅ Dev log generation (90%)
✅ Video creation (85%)
✅ Marketing posts (85%)
✅ Multi-platform distribution (80%)

### What Requires Human Input

🧠 Game design decisions (core concept, feel)
🧠 Code review and bug fixing
🧠 Art direction and curation
🧠 Video script approval
🧠 Marketing message approval
🧠 Community engagement
🧠 Final polish and "juice"

---

## Next Steps

1. **Setup** (Week 1): Install all tools, configure APIs
2. **Test** (Week 2): Run through pipeline with small test project
3. **Ship Game #4** (Weeks 3-6): Full production with automation
4. **Iterate** (Ongoing): Improve automation based on learnings

**This is the foundation for the entire JordanTheJet vertical.**

Once this works, clone the pattern to LuxeAI and CodeSensei.

Let's ship. 🚀
