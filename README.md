# 🎲 AI-Powered D&D Scenario Bot

**A Discord bot that generates dynamic D&D adventure scenarios, allowing players to interact asynchronously with an evolving narrative.**  

---

## 📌 Features
✅ **AI-Generated Adventures** – Unique D&D scenarios powered by OpenAI.  
✅ **Player Choices** – Interactive story progression via chat commands.  
✅ **Dice Rolling (`!roll d20`)** – RNG-based mechanics for skill checks. *(Coming Soon!)*  
✅ **Character Stats Tracking** – Store and use character attributes. *(Planned Feature!)*  
✅ **Drop-in & Asynchronous Play** – No scheduling needed, play at your own pace!  

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
| `!adventure` | Generates a new D&D adventure scenario. |
| `!roll d20` | Rolls a d20 for skill checks or combat. *(Coming Soon!)* |
| `!choose 1/2/3` | Selects an adventure path. *(Coming Soon!)* |
| `!register` | Creates a character profile. *(Planned Feature!)* |

### 📖 Example Adventure
```
📝 **Adventure Hook:**
A mysterious cave has been discovered in the forest, rumored to hold an ancient artifact. However, a spectral guardian blocks the way.

⚔️ Choices:
1. Battle the guardian head-on.
2. Solve the guardian’s riddle.
3. Offer a rare item as tribute.
```

---

## 🔧 Development Progress

### ✅ Completed
✔️ Set up Discord bot & API integration.  
✔️ AI-generated adventures using OpenAI.  
✔️ Optimized API usage (cooldowns, caching).  
✔️ Successfully deployed & tested first adventures.  

### 🚀 In Progress
🔲 Implement **dice rolling (`!roll d20`)**.  
🔲 Add **player choices (`!choose 1/2/3`)** for branching paths.  
🔲 Introduce **character stats tracking (`!register, !stats`)**.  

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