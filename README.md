# 🎲 AI-Powered D&D Scenario Bot

**A Discord bot that generates dynamic D&D adventure scenarios, allowing players to interact asynchronously with an evolving narrative.**  

---

## 📌 Features
✅ **AI-Generated Adventures** – Unique D&D scenarios powered by OpenAI.  
✅ **Player Choices (`!choose 1/2/3`)** – Interactive story progression via chat commands.  
✅ **Dice Rolling (`!roll d20`)** – RNG-based mechanics for skill checks and combat.  
✅ **Character Stats Tracking (`!register, !stats`)** – Strength, Dexterity, Intelligence impact gameplay.  
✅ **Hybrid AI Model** – GPT-3.5-Turbo for adventure generation, GPT-4 for intelligent decision-making.  
✅ **Drop-in & Asynchronous Play** – No scheduling needed, play at your own pace!  
✅ **Optimized API Usage** – Caching, rate-limiting, and structured prompts reduce OpenAI costs.  

---

## 🚀 Getting Started

### 1️⃣ Prerequisites
Before running the bot, ensure you have:
- **Python 3.8+** installed.
- A **Discord Developer Account** ([Create Here](https://discord.com/developers/applications)).
- An **OpenAI API Key** ([Get One Here](https://platform.openai.com/signup/)).
- Installed dependencies using `pip install -r requirements.txt`.

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
| `!choose 1/2/3` | Selects an adventure path. |
| `!register` | Creates a character profile with randomized stats. |
| `!stats` | Displays current character stats. |

### 📖 Example Adventure
```
📝 **Adventure Hook:**
A mysterious cave has been discovered in the forest, rumored to hold an ancient artifact. However, a spectral guardian blocks the way.

⚔️ **Choices:**
1️⃣ Battle the guardian head-on.
2️⃣ Solve the guardian’s riddle.
3️⃣ Offer a rare item as tribute.
```

---

## 🔧 Development Progress

### ✅ Completed
✔️ AI-generated adventures using OpenAI.  
✔️ Implemented `!choose` for interactive player decisions.  
✔️ Added `!roll d20` for dice mechanics.  
✔️ Character registration and stat tracking (`!register`, `!stats`).  
✔️ Hybrid AI model (GPT-3.5 for adventure, GPT-4 for decision-making).  
✔️ Implemented caching to reduce API costs.  
✔️ Refactored choice tracking to prevent errors.  
✔️ Optimized OpenAI prompts for better decision logic.  

### 🚀 In Progress
🔲 Allow player stats to influence dice rolls & AI-generated outcomes.  
🔲 Implement **NPC memory system** for interactive characters.  
🔲 Store persistent player choices for long-term game progression.  

### 🔜 Future Enhancements
📌 Character progression & inventory tracking.  
📌 More complex multi-stage adventures.  
📌 Multiplayer party mechanics.  

---

## 📜 Contributing
Want to help improve the bot? Fork the repo, submit a PR, or suggest new features in the **Issues tab**!

---

## 📜 License
MIT License. Feel free to modify and expand!

---

## 🌟 Credits
Created by **Professor_Alex** and contributors.  
Special thanks to **ChatGPT (by OpenAI)** for providing technical guidance, optimizations, and brainstorming throughout the development of this project.  
