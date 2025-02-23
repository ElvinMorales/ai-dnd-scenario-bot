# 📜 AI-Powered D&D Scenario Bot - Development Roadmap

## 🔥 Project Overview

An AI-powered Discord bot that generates dynamic D&D adventure scenarios, enabling players to experience interactive narratives with traditional RPG mechanics. The bot leverages OpenAI models to produce creative content and intelligent outcomes.

---

## ✅ Completed Milestones

- **Foundation:**
  - Set up the GitHub repository, initial README, LICENSE, and .gitignore.
  - Configured environment variables via `.env` for Discord and OpenAI API keys.
  - Created `requirements.txt` for dependency management.

- **Core Gameplay Mechanics:**
  - Implemented `!adventure` command for AI-generated scenarios.
  - Developed `!choose` command for interactive decision-making.
  - Added basic dice rolling with `!roll d20`.
  - Built player registration and stat tracking (`!register` and `!stats`).
  - Integrated cooldown systems to prevent command spam.

---

## 🚀 In Progress (Immediate Next Steps)

### 1. Intelligent Decision Tracking & Persistence
- **Player Stat Bonuses & Dice Rolls:**  
  - **Task:** Integrate player stat modifiers into the dice rolling function.
  - **Status:** Completed.

- **Expanded Character Stats:**
  - **Task:** Update the `!register` command to generate a full D&D 5e character with six ability scores (Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma) and calculate HP dynamically using Constitution.
  - **Status:** Completed.
  
- **Revised Dice Roll Commands:**
  - **Task:** Modify `!roll d20` so that if no ability is provided it returns a plain roll, and if an ability is specified, it applies the corresponding modifier.
  - **Status:** Completed.
  
- **Updated Stats Display:**
  - **Task:** Update `!stats` command to show all six abilities along with their calculated modifiers and the current HP.
  - **Status:** Completed.

- **Database Integration:**  
  - **Task:** Implement SQLite to store player choices and history persistently.
  - **Status:** Completed.
  
### 2. Documentation & Code Quality Enhancements
- **Update Documentation:**  
  - **Task:** Ensure README and inline comments are current with new features.
  - **Status:** Ongoing.

- **Code Refactoring:**  
  - **Task:** Remove debugging code and clean up command handlers.
  - **Status:** Completed.

- **Testing:**
  - **Task:** Conduct further testing of new features, including edge cases (e.g., unregistered users using modifier commands) and refine any remaining bugs.
  - **Estimated Timeline:** Ongoing.



---

## 🛠 Planned Enhancements (Future Features)

### AI-Enhanced Gameplay Features
- **Context-Specific Rolls:**
  - Separate commands for different types of rolls (e.g., attack, saving throws, skill checks) that apply the correct ability modifiers.
- **Interactive NPCs:**  
  - Introduce pre-defined AI-driven NPCs with unique personalities.
- **NPC Memory System:**  
  - Enable NPCs to remember past player interactions.
- **Dynamic Encounter Scaling:**  
  - Adjust challenge difficulty based on player performance and history.

### Expanded RPG Mechanics
- **Character Progression:**  
  - Implement an XP and leveling system.
- **Inventory Tracking:**  
  - Track items and rewards through adventures.

### Data Visualization & Analytics
- **Dashboard Creation:**  
  - Develop a Power BI or web dashboard to visualize player trends and decision pathways.
- **User Feedback Collection:**  
  - Implement mechanisms for beta testing and collecting user feedback.

---

## 📊 Feedback, Testing, & Contributor Onboarding

- **User Testing:**  
  - Organize beta tests with a small group of users.
  - Prepare a testing plan covering:
    - Functionality tests for all commands.
    - Edge case testing (e.g., unregistered users, invalid input).
    - Beta testing feedback integration.
- **Documentation for Contributors:**  
  - Create an onboarding guide detailing the development environment setup, code style, and testing procedures.
- **Regular Updates:**  
  - Schedule periodic reviews of project progress and update the roadmap as needed.

---

## 🏁 Final Features & Testing (Planned Release)

- **Beta Testing:**  
  - Gather and incorporate user feedback to fine-tune gameplay.
- **Performance Optimization:**  
  - Conduct a final review of API usage and bot performance.
- **Final Documentation:**  
  - Ensure all documentation, including the contributor guide, is comprehensive and up-to-date.