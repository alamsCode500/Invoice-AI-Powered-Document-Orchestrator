# 🚀 Invoice AI — Document Orchestrator

A lightweight Streamlit + Gemini + n8n application that extracts key invoice details using AI and triggers automated alert emails based on conditions.

# ⭐ Features

Upload invoice PDFs

Gemini AI extracts invoice details

Clean UI showing four final outputs

“Send Alert Mail” button triggers n8n automation

Secure credentials using st.secrets

# 📁 Project Structure
app.py
requirements.txt
.streamlit/secrets.toml
PDFs/        ← sample invoices
README.md

# 🛠 Local Setup
pip install -r requirements.txt
streamlit run app.py


Add your secrets in:

.streamlit/secrets.toml

# ☁️ Deploy on Streamlit Cloud

Push repo to GitHub

Open Streamlit Cloud → New App

Select repo

Add secrets → Deploy

# 🔁 n8n Workflow (Required Nodes)

Webhook Trigger (POST)

AI Analysis Node

IF Condition

Email Draft Node

Email Node

Respond to Webhook (returns JSON)

# ✔ What to Test

PDF uploads correctly

Gemini extracts invoice data

Conditional email triggers via button

All outputs render cleanly in UI

UI View:
<img width="1920" height="3337" alt="image" src="https://github.com/user-attachments/assets/be5e1e39-0025-4569-976d-df634a0215ae" />
