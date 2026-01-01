# 🧾 Invoice AI — Document Orchestrator
GenAI · Python · Streamlit · n8n · Automation · Gemini API

# 📌 Project Overview

Invoice AI — Document Orchestrator is an AI-powered invoice intelligence and automation system that extracts structured data from invoices, answers user-specific questions, assesses financial risk, and automatically triggers workflow actions (email alerts) using n8n.

This project demonstrates my ability to build production-style AI pipelines, combining:

* Document processing

* Generative AI (Gemini)

* Business rule–based risk evaluation

* Workflow orchestration

* Human-in-the-loop automation

# 🎯 Business Problem

Organizations receive large volumes of invoices that:

* Require manual review

* Have varying formats (PDF/TXT)

* Contain high-risk, high-value payments

* Need approvals and alerts based on business rules

This project automates that process by:

* Extracting invoice intelligence using GenAI

* Identifying financial risk automatically

* Triggering alerts only when required

* Returning clean, structured responses via API

# 🧠 Solution Architecture

User → Streamlit UI

        ↓

Invoice Upload (PDF/TXT)

        ↓

Text Extraction (pdfplumber / PyMuPDF)

        ↓

Gemini AI (Structured JSON Extraction)

        ↓

Risk Classification (Low / Medium / High)

        ↓

n8n Workflow Orchestration

        ↓

Conditional Email Alert

        ↓

Final Response to User

# 🔧 Tech Stack

# 🖥 Frontend

* Streamlit – Interactive UI for uploads, questions, and results

# 🤖 AI & NLP

* Google Gemini 2.5 Flash API

* Schema-driven structured JSON extraction

* Deterministic output (temperature = 0)

# 📄 Document Processing

* pdfplumber

* PyMuPDF (fallback)

* TXT file support

# 🔁 Automation & Orchestration

* n8n

* Webhooks

* Conditional workflows

* Email notifications

# 📦 Backend & Utilities

* Python

* Requests

* JSON schema validation

# 📊 Key Features

# ✅ Intelligent Invoice Understanding

* Extracts key invoice fields:

  * Vendor

  * Invoice number

  * Invoice date

  * Due date

  * Total amount

* Confidence score & reasoning for each field

# ✅ Dynamic Question Answering

Users can ask focused questions such as:

* “What is the due date?”

* “What is the total amount?”

* “Who is the vendor?”

AI returns only relevant, explainable fields.

# ⚠️ Automated Risk Classification

Invoices are automatically classified based on total amount:

Risk Level	Rule

High	      Amount > 50,000

Medium	    5,000 – 50,000

Low	        < 5,000


# ✉️ Conditional Email Automation (n8n)

* High-risk invoices → Email alert sent

* Low/Medium risk → No email

* Fully automated, rule-based decisioning

# 🔁 n8n Workflow Highlights

* Webhook-based orchestration

* Gemini-powered analysis node

* JSON parsing & validation

* Conditional branching (IF risk == High)

* SMTP-based email notification

* Structured webhook response

# 🖼 Streamlit Application Flow

* Upload invoice (PDF or TXT)

* Ask a business question

* View:

* * Extracted structured JSON

* * AI-generated invoice summary

* Enter recipient email

* Trigger automation

* Receive:

* * Final analytical answer

* * Email content

* * Automation status

# 📂 Project Structure
Invoice-AI-Document-Orchestrator/
│
├── app.py                      # Streamlit application
├── requirements.txt            # Dependencies
├── README.md                   # Project documentation
└── n8n_workflow.json           # Invoice automation workflow

# ⚙️ Setup & Installation

# 1️⃣ Clone Repository

git clone https://github.com/your-username/invoice-ai-orchestrator.git
cd invoice-ai-orchestrator

# 2️⃣ Install Dependencies

pip install -r requirements.txt

# 3️⃣ Configure Secrets

Create .streamlit/secrets.toml:

GEMINI_API_KEY = "your_gemini_api_key"
N8N_WEBHOOK_URL = "your_n8n_webhook_url"

# 4️⃣ Run Application

streamlit run app.py

# 🧠 Key Learnings

* Schema-based prompting for reliable LLM output

* Handling messy, unstructured documents

* AI + rule-based hybrid decision systems

* Workflow orchestration with external tools

* Designing explainable AI responses

# 👤 Author

Tauseef Alam

Aspiring Data Scientist / AI Engineer

Python | GenAI | Automation | SQL | Streamlit | n8n

UI Look:
<img width="1920" height="3337" alt="image" src="https://github.com/user-attachments/assets/be5e1e39-0025-4569-976d-df634a0215ae" />
