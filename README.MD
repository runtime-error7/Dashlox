<div align="center">

# ⚡ DASHLOX

**Your 100% Offline, Privacy-First AI Data Analyst.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Offline](https://img.shields.io/badge/Status-100%25_Offline-emerald.svg)]()
[![Local AI](https://img.shields.io/badge/AI-Ollama_Powered-blue.svg)]()

*Drop a CSV. Chat with your data. Eject production-ready code. Zero internet required.*

</div>

---

## 🛑 The Problem
You have sensitive financial data, private user logs, or confidential company metrics. You want to use the power of AI data analysts (like ChatGPT Advanced Data Analysis), but **you cannot legally or safely upload your data to the cloud.** ## 🟢 The Solution: Dashlox
Dashlox is a blazing-fast, desktop-native web app powered by **DuckDB** and **Local LLMs (via Ollama)**. It runs entirely on your machine. Your data never leaves your hard drive. 

![Dashlox Demo](https://via.placeholder.com/800x400.png?text=Put+A+15-Second+GIF+Demo+Here!)
*(Note to dev: Record a quick screen-capture GIF of you dropping a file and generating a chart, then replace the link above!)*

---

## ✨ God-Mode Features

* 📂 **The Magic Drop Zone:** No uploads. No database configurations. Just drag and drop a `.csv`, `.json`, or `.xlsx` into the `data_in/` folder, and Dashlox instantly converts it into a lightning-fast in-memory SQL database.
* 🤖 **Conversational UI Engine:** Type *"Make a neon green bar chart of Q3 revenue,"* and the local 1.5B parameter AI writes the exact Chart.js configuration in milliseconds.
* ⚡ **Eject to Code:** Stop recreating charts manually. Click the "Eject" button to instantly copy the production-ready React/JS code for your generated charts directly to your clipboard.
* 🔒 **100% Air-Gapped:** Turn your Wi-Fi off. Dashlox bundles Tailwind, Chart.js, and the AI models locally. Zero telemetry. Zero data leaks.

---

## 🚀 One-Click Installation (Windows)

We built Dashlox so you don't have to fight with Python environments or dependency hell. 

1. **[Download Dashlox_Setup.exe](https://github.com/YOUR_GITHUB_USERNAME/Dashlox/releases/latest/download/Dashlox_Setup.exe)** from the Releases page.
2. Double-click to run it.
3. The setup will automatically build your desktop workspace, pull the lightweight AI weights via Ollama, and place a launch icon on your Desktop.

**Boom. You are ready to analyze.**

---

## 🏗️ Architecture & Tech Stack

Dashlox is built for speed and efficiency on consumer hardware:

* **Data Engine:** `DuckDB` (Handles massive CSVs instantly without crashing RAM).
* **AI Engine:** `Qwen2.5:1.5b` running natively via `Ollama`. Small enough for laptops, smart enough for perfect JSON output.
* **Backend:** `FastAPI` + `Python Watchdog` (for real-time folder monitoring).
* **Frontend:** `Vanilla JS` + `TailwindCSS` + `Chart.js` (Bundled locally).

---

## 👨‍💻 For Developers: Running from Source

Want to build on top of Dashlox or run it on Mac/Linux?

```bash
# 1. Clone the repository
git clone [https://github.com/YOUR_GITHUB_USERNAME/Dashlox.git](https://github.com/YOUR_GITHUB_USERNAME/Dashlox.git)
cd Dashlox

# 2. Install dependencies
pip install -r requirements.txt

# 3. Ensure Ollama is running, then start the server
./start.sh

## 📖 How to Use Dashlox (The Manual)

Using Dashlox is designed to feel like magic. No configuration, no cloud accounts. 

### Step 1: The Drop
Navigate to the `Dashlox_Workspace/data_in/` folder on your Desktop. Drag and drop any raw `.csv`, `.xlsx`, or `.json` file into this folder. 
*(Example: Drop your messy `sales_data_2024.csv` here).*

### Step 2: The Launch
Double-click the **Dashlox** icon on your Desktop. A local server will boot up, and your default web browser will instantly open to `http://localhost:3000`. 

### Step 3: Verify the Connection
Look at the top right of the dashboard. You should see a green badge saying **🟢 Loaded: sales_data_2024**. The AI has already read your columns and prepared the database.

### Step 4: Chat to Visualize
Use the chatbox on the right side. Be direct! Try prompts like:
* *"Make a bar chart comparing Revenue and Expenses."*
* *"Change the chart type to a line graph."*
* *"Make the revenue line neon green and the expenses line red."*

### Step 5: Eject to Code ⚡
Once the AI generates the perfect chart on your screen, click the purple **Eject Code ⚡** button. Dashlox will instantly copy the raw, production-ready `Chart.js` configuration to your clipboard. Paste it directly into your company's React, Vue, or HTML codebase!

