import streamlit as st
import io
import json
import requests
import pdfplumber
from typing import Dict, Any
import google.generativeai as genai

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="Invoice AI Orchestrator", layout="wide")
st.markdown("<h1 style='text-align:center; color:#4B8BBE;'>Invoice AI-Powered Document Orchestrator</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>Upload an invoice (PDF/TXT), ask a focused question, extract structured fields with Gemini, "
    "and optionally trigger a conditional n8n automation (Send Alert Mail).</p>", unsafe_allow_html=True
)

# -----------------------
# Secrets check
# -----------------------
if "GEMINI_API_KEY" not in st.secrets or "N8N_WEBHOOK_URL" not in st.secrets:
    st.error("Missing secrets. Add GEMINI_API_KEY and N8N_WEBHOOK_URL to Streamlit Cloud Secrets.")
    st.stop()

GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
N8N_WEBHOOK = st.secrets["N8N_WEBHOOK_URL"]

# Initialize Gemini (Google Generative AI)
genai.configure(api_key=GEMINI_KEY)

# -----------------------
# Text extraction helpers
# -----------------------
def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_chunks = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_chunks.append(t)
    except Exception as e:
        st.warning(f"pdfplumber failed: {e}")
        try:
            import fitz
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                text_chunks.append(page.get_text())
            doc.close()
        except Exception as e2:
            st.error(f"PDF extraction fallback failed: {e2}")
            return ""
    return "\n\n".join(text_chunks)

def extract_text_from_txt(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8", errors="replace")
    except Exception:
        return file_bytes.decode("latin-1", errors="replace")

# -----------------------
# Gemini extraction
# -----------------------
INVOICE_SCHEMA = {
    "title": "InvoiceExtraction",
    "type": "object",
    "properties": {
        "extracted_pairs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "value": {"type": "string"},
                    "confidence": {"type": "number"},
                    "reason": {"type": "string"}
                },
                "required": ["key", "value"]
            }
        },
        "risk_level": {"type": "string"},
        "summary": {"type": "string"}
    },
    "required": ["extracted_pairs"]
}

SYSTEM_PROMPT = (
    "You are an assistant that MUST output only valid JSON matching the provided schema. "
    "You will be given an INVOICE document and a USER QUESTION. "
    "Identify the 5–8 most relevant key/value pairs that help answer the user's question. "
    "For each pair, include 'reason' and 'confidence' (0.0 - 1.0). "
    "Determine the 'risk_level' based on the invoice total amount as follows: "
    "High: total amount greater than 50,000; "
    "Medium: total amount between 5,000 and 50,000; "
    "Low: total amount less than 5,000; "
    "Use 'Unknown' if the total amount cannot be determined. "
    "Also include a short 'summary' of the invoice."
)

def call_gemini(document_text: str, user_question: str) -> Dict[str, Any]:
    user_prompt = (
        f"DOCUMENT:\n\"\"\"{document_text[:30000]}\"\"\"\n\n"
        f"USER QUESTION:\n\"\"\"{user_question}\"\"\"\n\n"
        f"SCHEMA:\n{json.dumps(INVOICE_SCHEMA)}\n\n"
        "STRICT RULES:\n"
        "- Output ONLY valid JSON.\n"
        "- Do NOT use backticks.\n"
        "- Do NOT return markdown.\n"
        "- Do NOT explain.\n"
        "- Only return JSON matching the schema.\n"
    )

    try:
        # Use official google-generativeai client
        response = genai.chat.create(
            model="gemini-1.5-chat",  # Streamlit Cloud compatible model
            messages=[{"role": "user", "content": SYSTEM_PROMPT + "\n\n" + user_prompt}],
            temperature=0.0,
            max_output_tokens=1500
        )
        raw_text = response.candidates[0].content[0].text
    except Exception as e:
        return {"error": f"Gemini API call failed: {e}"}

    cleaned = raw_text.strip().replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except Exception as e:
        return {"raw_output": cleaned, "parse_error": str(e)}

# -----------------------
# Streamlit UI
# -----------------------
uploaded_file = st.file_uploader("Upload Invoice (PDF or TXT)", type=["pdf", "txt"])
user_question = st.text_input("❓ Ask a specific question about the invoice", placeholder="E.g., 'What is the total amount and due date?'")

if uploaded_file and user_question:
    file_bytes = uploaded_file.read()
    raw_text = extract_text_from_pdf(file_bytes) if uploaded_file.name.lower().endswith(".pdf") else extract_text_from_txt(file_bytes)

    if not raw_text:
        st.error("No text extracted from the document.")
        st.stop()

    # Document Preview
    with st.expander("Document Preview (first 2000 chars)"):
        st.code(raw_text[:2000] + ("...\n\n[truncated]" if len(raw_text) > 2000 else ""), language="text")

    # Gemini Extraction
    st.info("Running Gemini dynamic extraction...")
    extraction = call_gemini(raw_text, user_question)
    st.success("Extraction complete.")
    st.subheader("Structured Data Extracted (JSON)")
    st.json(extraction)

    # Email Automation
    st.subheader("Email Automation (n8n)")
    recipient = st.text_input("Recipient Email ID", placeholder="approver@example.com")
    send_button = st.button("Send Alert Mail")

    if send_button:
        if not recipient:
            st.warning("Please provide a recipient email before sending.")
        else:
            payload = {
                "document_text": raw_text[:50000],
                "extracted_json": extraction,
                "user_question": user_question,
                "recipient_email": recipient,
                "file_name": uploaded_file.name
            }
            with st.spinner("Calling n8n webhook..."):
                try:
                    r = requests.post(N8N_WEBHOOK, json=payload, headers={"Content-Type": "application/json"}, timeout=60)
                    r.raise_for_status()
                    n8n_resp = r.json()
                    st.success("Webhook called successfully.")
                except Exception as e:
                    st.error(f"Failed to call n8n webhook: {e}")
                    n8n_resp = {"error": str(e)}

            # Process n8n response
            try:
                if isinstance(n8n_resp, list):
                    n8n_data = n8n_resp[0].get("json", n8n_resp[0]) if n8n_resp else {}
                elif isinstance(n8n_resp, dict):
                    n8n_data = n8n_resp.get("json", n8n_resp)
                else:
                    n8n_data = {}

                final_answer = n8n_data.get("final_answer") or n8n_data.get("finalAnswer")
                email_body = n8n_data.get("email_body") or n8n_data.get("emailBody")
                status = n8n_data.get("automation_status") or n8n_data.get("status")

                with st.expander("Final Analytical Answer"):
                    st.info(final_answer if final_answer else "No analytical answer returned by n8n")

                with st.expander("Generated Email Body"):
                    st.code(email_body if email_body else "No email body returned", language="text")

                with st.expander("Email Automation Status"):
                    if status:
                        if str(status).lower() in ["sent", "ok", "succeeded", "true"]:
                            st.success(f"Email Status: {status}")
                        else:
                            st.warning(f"Email Status: {status}")
                    else:
                        st.info("No automation status returned by n8n")

            except Exception as e:
                st.error(f"Error processing n8n response: {e}")
                st.subheader("Raw n8n Response")
                st.json(n8n_resp)

else:
    st.info("ℹ️ Upload an invoice and ask a question to begin.")
