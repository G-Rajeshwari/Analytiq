# 📊 Analytiq — AI-Powered Business Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-purple)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

> **Upload any CSV or Excel file, ask questions in plain English, and get instant AI-powered insights, charts, and chart analysis — no SQL, no code required.**

🔗 **Live Demo:** [analytiq-rajeshwari.streamlit.app](https://analytiq-rajeshwari.streamlit.app)

---

##  What is Analytiq?

Analytiq is a multimodal AI analytics platform that turns raw data files into business insights in seconds. It combines natural language processing, interactive visualizations, and AI vision — all in one clean interface.

Built for data analysts, business users, and anyone who works with data but doesn't want to write code every time they need an answer.

---

##  Features

###  Tab 1 — Data Analysis
- Upload **CSV or Excel** files instantly
- Auto-generates **KPI cards** (row count, columns, missing values, numeric stats)
- Interactive **charts**: bar, line, scatter, histogram, box plot — all with Plotly
- **Date filtering** by any date column
- Download filtered data as CSV

###  Tab 2 — Chat with Your Data
- Ask questions in **plain English** — "What is the average revenue by region?"
- Powered by **Groq LLaMA 3.1** for fast, accurate responses
- AI understands your column names and data context automatically
- No SQL, no code — just natural conversation

###  Tab 3 — AI Vision (Chart Analysis)
- Upload **any chart image** (PNG, JPG)
- AI reads and interprets the chart — trends, outliers, key takeaways
- Works on charts from Power BI, Excel, Tableau, or anywhere
- Perfect for quickly summarizing dashboards you didn't build

---

##  Tech Stack

| Technology | Role |
|---|---|
| Python | Core language |
| Streamlit | Web app framework |
| Groq API (LLaMA 3.1-8b) | NLP chat + AI Vision |
| Plotly | Interactive charts |
| Pandas | Data manipulation |
| OpenPyXL | Excel file support |

---

##  Project Structure

```
Analytiq/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── secrets.example.toml    # API key template
├── .gitignore              # Excludes .venv, secrets
└── README.md
```

---

##  Setup & Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/G-Rajeshwari/Analytiq.git
cd Analytiq
```

### 2. Create virtual environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\Activate.ps1
# Mac/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```
Get a free API key at [console.groq.com](https://console.groq.com)

### 5. Run the app
```bash
streamlit run app.py
```

---

##  API Key Security

- API key is stored in `.streamlit/secrets.toml` (excluded from git via `.gitignore`)
- Never hardcode API keys in source files
- See `secrets.example.toml` for the required format

---

##  Author

**G. Rajeshwari**  
🔗 [GitHub](https://github.com/G-Rajeshwari) | [LinkedIn](https://linkedin.com/in/rajeshwari)  
🌐 Live: [analytiq-rajeshwari.streamlit.app](https://analytiq-rajeshwari.streamlit.app)
