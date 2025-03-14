# 📜 AI-Powered D&D Scenario Bot - Development Roadmap

## 🔥 Project Overview

An AI-powered Discord bot that generates dynamic D&D adventure scenarios, blending interactive storytelling with traditional D&D 5e mechanics. The bot leverages OpenAI models to create immersive experiences, complete with a full character creation system, dice rolling mechanics, and skill-based gameplay.

---
## ✅ Completed Milestones

### **1. Foundation**
- Set up the GitHub repository, initial README, LICENSE, and `.gitignore`.
- Configured environment variables via `.env` for Discord and OpenAI API keys.
- Created `requirements.txt` for dependency management.

### **2. Core Gameplay Mechanics**
- Implemented `!adventure` command for AI-generated scenarios.
- Developed `!choose` command for interactive decision-making.
- Built **player registration and full stat tracking** (`!register` and `!stats`).
- Integrated a **cooldown system** to prevent command spam.
- Implemented **decision tracking and persistence** using SQLite.

### **3. Expanded Dice Rolling System**
- Implemented `!roll d20` (simple d20 roll).
- Enhanced `!roll d20 <ability>` to apply the correct ability modifier.
- Added context-specific rolls:
  - **`!attack`** → Uses **Strength** for melee attacks.
  - **`!ranged`** → Uses **Dexterity** for ranged attacks.
  - **`!save <ability>`** → Rolls a saving throw based on the specified ability.
- **Skill Checks Implemented!**
  - **`!skill <skill_name>`** → Rolls a skill check with the corresponding ability modifier.
  - **`!skills`** → Displays the full list of skills and their linked abilities.

### **4. Character Management & Customization**
- Players can now **choose Name, Race, and Class** during `!register`.
- **Ability scores are displayed before class selection** to help players make better choices.
- Implemented `!reset` → Allows players to delete and re-register.
- Implemented `!graveyard` → Lets players retrieve past deleted characters.


---
## 🚀 In Progress (Immediate Next Steps)

### **1. Proficiency Bonuses for Skills**
- **Task:** Implement proficiency bonuses so players who are proficient in certain skills gain an additional bonus when rolling skill checks.
- **Estimated Timeline:** 1 week.

### **2. Expanding `!graveyard`**
- **Task:** Modify `!graveyard` to store multiple past characters instead of just the most recent one.
- **Estimated Timeline:** Future update.

### **3. Expanded Documentation & Code Optimization**
- **Task:** Refine the bot’s documentation, particularly covering decision tracking and how skills function.
- **Estimated Timeline:** Ongoing, with updates scheduled alongside new features.

---

## 🛠 Planned Enhancements (Future Features)

### **1. AI-Enhanced Gameplay Features**
- **Interactive NPCs:** Introduce AI-generated NPCs with unique personalities and memory systems.
- **Decision-Based Adventure Continuity:** Allow **past choices to influence future scenarios** beyond a single adventure session.

### **2. RPG Mechanics Enhancements**
- **Character Progression:** Implement an **XP and leveling system**.
- **Inventory & Items:** Add **item tracking** for player rewards.
- **Custom Character Creation:** Let players **manually assign ability scores** instead of rolling randomly.

### **3. Data Visualization & User Analytics**
- **Player Statistics Dashboard:** Create a dashboard to **track player trends**, **decision patterns**, and **success rates**.
- **Adventure Analytics:** Analyze common adventure outcomes and refine AI generation for better balance.

---

## 📊 Contributor Onboarding & Testing

- **Contributor Guide:** Develop an onboarding guide for new contributors, covering:
  - Project structure
  - Setting up the development environment
  - Code style guidelines
  - Best practices for testing
  
- **Testing Plan:** Prepare structured tests for:
  - **Functionality testing** (commands working as intended).
  - **Edge case testing** (invalid input handling, unregistered users).
  - **Load testing** (ensuring performance stability under multiple users).

---

## 🏁 Final Features & Public Release

- **Beta Testing:** Conduct a beta phase with real users to gather feedback.
- **Performance Optimization:** Final review of API usage and bot performance.
- **Final Documentation & Deployment:** Ensure the project is ready for public use.