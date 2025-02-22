# 🎲 AI-Powered D&D Scenario Bot

**A Discord bot that generates dynamic D&D adventure scenarios, allowing players to interact asynchronously with an evolving narrative.**

---

## Overview
AI-Powered D&D Scenario Bot is designed to create engaging and unique D&D adventures on Discord. It leverages OpenAI’s GPT models to generate adventure hooks, interactive choices, and dynamic outcomes, all while providing traditional RPG mechanics such as dice rolling and character stat tracking.

---

## 📌 Features
- **AI-Generated Adventures:** Unique scenarios powered by GPT-3.5-Turbo (with GPT-4 for enhanced decision outcomes).
- **Interactive Player Choices:** Progress the story using commands like `!choose 1/2/3`.
- **Dice Rolling Mechanics:** Use `!roll d20` to simulate skill checks and combat.
- **Character Registration & Stats:** Register your character with `!register` and view your attributes using `!stats`.
- **Optimized API Usage:** Caching, rate-limiting, and structured prompts reduce API costs.
- **Hybrid AI Model:** Combining GPT-3.5 for general content with GPT-4 for intelligent decision-making.

---

## 🚀 Getting Started

### Prerequisites

Before running the bot, make sure you have:
- **Python 3.8+** installed.
- A **Discord Developer Account** to create and manage your bot ([Create Here](https://discord.com/developers/applications)).
- A **Discord Bot Token**.
- An **OpenAI API Key** ([Get One Here](https://platform.openai.com/signup)).
- Installed dependencies via:
  ```bash
  pip install -r requirements.txt
---

### 2️⃣ Installation & Setup

#### **Step 1: Clone the Repository**
```bash
git clone https://github.com/YOUR-USERNAME/ai-dnd-scenario-bot.git
cd ai-dnd-scenario-bot
```

#### **Step 2: Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

#### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **Step 4: Set Up API Keys**
1. **Create a `.env` file** in the project folder:
```ini
DISCORD_TOKEN=your-discord-bot-token-here
OPENAI_API_KEY=your-openai-api-key-here
```
2. **Save the file** (This keeps your keys secure!).

---

### 3️⃣ Running the Bot
```bash
python bot.py
```
✅ The bot will log in to Discord and wait for commands!

---

## 🎮 How to Play

### 🔹 Available Commands
| Command | Description |
|---------|-------------|
| `!adventure` | Generates a new AI-powered D&D adventure scenario. |
| `!roll d20` | Rolls a d20 for skill checks or combat. |
| `!choose 1/2/3` | Selects an adventure path from the available choices. |
| `!register` | Registers a new character with random stats. |
| `!stats` | Displays current character stats. |

### 📖 Usage Example
```yaml
User: !register
Bot: @Player, you have been registered! Use `!stats` to view your attributes.

User: !stats
Bot: 📜 **Player's Stats:**
     💪 Strength: 15
     🏹 Dexterity: 12
     🧠 Intelligence: 17
     ❤️ HP: 100

User: !adventure
Bot: 🎲 Generating a new adventure... please wait!
     📜 **Adventure Hook:**
     A mysterious cave beckons in the dark forest...
     ⚔️ **Choices:**
     1️⃣ Enter the cave.
     2️⃣ Circumvent the cave.
     3️⃣ Set up camp nearby.
     Use `!choose 1`, `!choose 2`, or `!choose 3` to decide your action!

User: !choose 1
Bot: 🔮 You chose: Enter the cave.
     🎲 Your roll: 14
     📝 **Outcome:** As you step into the cave, you discover ancient inscriptions...
```
---
## 🛠 Technologies & Dependencies
- **Python 3.8+**
- **Discord.py** for interacting with the Discord API
- **OpenAI API** for generating AI content
- **dotenv** for environment variable management
---
## ⚠️ Known Issues
- Adventure caching may occasionally reuse outdated choices.
- Stat-based modifiers for dice rolls are in progress.
- Some dynamic outcomes may vary in consistency; further tuning is needed.
---
## 🤝 Contributing
Contributions are welcome! Please follow these guidelines:
- **Code Style:** Follow PEP8 guidelines and ensure your code is well-commented.
- **Pull Requests:** Submit a clear PR with detailed descriptions of changes and reference any related issues.
- **Testing:** Ensure your changes are tested locally before submission.
- **Documentation**: Update the README and inline documentation if your changes affect functionality.

Feel free to fork the repository, experiment, and propose enhancements via the Issues tab.

---

## 📜 License
MIT License. Feel free to modify and expand!

---

## 🌟 Credits
Created by **Professor_Alex** and contributors.  
Special thanks to **ChatGPT (by OpenAI)** for providing technical guidance, optimizations, and brainstorming.