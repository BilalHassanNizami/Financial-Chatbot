---
license: mit
title: Financial Chatbot
sdk: gradio
emoji: 🏆
colorFrom: indigo
colorTo: green
pinned: true
short_description: AI Powered Financial Chatbot
sdk_version: 5.38.2
---

title: Financial Chatbot
emoji: 🏆
colorFrom: indigo
colorTo: green
sdk: gradio
app_file: app.py
pinned: false
license: mit
---

# 💰 AI-Powered Financial Chatbot

Welcome to the **Financial Chatbot**, an AI-driven tool designed to answer financial queries about **Apple**, **Microsoft** and **Tesla** 
using their annual financial reports(Form 10-K) filed with US SEC from **2022 to 2024**.

Built for the **Boston Consulting Group(BCG X) GenAI Job Simulation**

## 🔐 License:

- This project is released under the MIT License.

## 📦 Tech Stack:

- Python
- Pandas for data handling
- Plotly for chart visualization
- Hugging Face Spaces for deployment

## 📁 Files Included:

- app.py: *Main Gradio interface*
- chatbot_cleaned.csv: *Cleaned financial dataset*
- README.md: *This file*
- requirements.txt: *Python dependencies*
  
## 🚀 How to Run

1. **Install dependencies**  
   Run the following in terminal:
pip install -r requirements.txt

2. **Launch chatbot**
python chatbot_app.py

3. **Visit the Gradio link** in your browser to start asking financial questions!


## 🚀 How It Works:

- This chatbot processes user queries

- infers missing information (like company or year)

- fetches relevant data from a pre-cleaned CSV and returns a response — optionally with a plot or comparison.

- Short or vague queries

- Year ranges like "last year" or "last 2 years"


 ## 🧠 Example Questions You Can Ask:

→ Compare net income of Apple and Tesla in 2023  
→ Show revenue trend for Microsoft  
→ Which company had the highest R&D expense in 2024?  
→ How much did Tesla earn last year?  
→ Give EPS basic/EPS diluted of all companies for all years  
→ Who had better Free Cash Flow in 2023?  
→ Show bar chart of revenue for all companies across years 

 ## Features:

- Natural language understanding
- Company & year inference
- Cross-company comparisons
- Multi-year trend analysis
- Chart generation (bar plots)
- Conversational memory
- Supports vague or shorthand questions
- Based on cleaned financial data from 10-K Forms
- Covers 14+ financial metrics and 3 major companies

---

**Disclaimer:**
📌 This project is publicly visible for educational and portfolio purposes only.  
❌ Reuse, modification, or redistribution of the code is not permitted without permission.

---

Built by **Bilal Hassan Nizami** (Data Analyst/Scientist)  
GenAI Consulting Team – Boston Consulting Group (BCG X) - Forage Job Simulation