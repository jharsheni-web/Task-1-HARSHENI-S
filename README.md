📊 Project 1: Zero-Shot & Few-Shot Data Extraction

Batch: 2026 | Powered by: DecodeLabs

---

📌 Project Overview

This project demonstrates deterministic data extraction from unstructured customer support emails using Large Language Models (LLMs). The goal is to transform chaotic, messy text into clean, structured JSON with absolute precision – without hallucinations or conversational filler.

🎯 Key Objectives

· Extract exactly 5 variables from raw email text
· Enforce strict JSON output (no extra text)
· Implement Few-Shot learning with 2-3 perfect examples
· Use delimiters to separate instructions from data
· Return null for missing fields (no hallucinations)
· Achieve >99% format adherence using temperature = 0

---

🧩 The Five Variables

Field Type Description
customer_name String Full name of the customer
order_number String Order ID (e.g., ORD-1234)
complaint_type Enum "billing", "shipping", "product", or "other"
severity_level Integer 1 (low) to 5 (critical)
contact_phone String or null Phone number; null if not provided

---

🛠️ Tech Stack

Component Technology
IDE VS Code
Language Python 3.8+
LLM Backend Groq API (cloud) OR Ollama (local)
Key Libraries groq, python-dotenv, requests (for Ollama)
Environment .env for API keys (Groq)

---

📁 Project Structure

```
email_extractor/
│
├── extract.py              # Main script (Groq API version)
├── extract_local.py        # Main script (Ollama local version)
├── .env                    # API key (for Groq) – not committed
├── .gitignore              # Prevents .env from being uploaded
├── test_email.txt          # Optional: test email input
├── output.json             # Optional: saved extraction result
└── README.md               # This file
```

🚀 How to Run the Project

Using Ollama (Fully Local – No API Key)

1. Prerequisites

· Ollama installed
· A local model downloaded:

```bash
ollama pull llama3.2:3b
```

2. Setup

```bash
# Install Python requests library
pip install requests
```

3. Create extract_local.py

Copy the script from below.

4. Run

```bash
python extract_local.py
```

---

📝 Core Extraction Prompt

The prompt uses strict delimiters ("""), Few-Shot examples, and a clear instruction set:

```
You are a strict data extraction engine. Output ONLY valid JSON.

Extract: customer_name, order_number, complaint_type (billing/shipping/product/other), severity_level (1-5), contact_phone (or null if missing).

Few-shot examples:
Input: Alice. Order ORD-1234 lost. Call 555-1234. Urgent.
Output: {"customer_name":"Alice","order_number":"ORD-1234","complaint_type":"shipping","severity_level":5,"contact_phone":"555-1234"}

Input: Bob. Order ORD-5678 wrong item. Not urgent. No phone.
Output: {"customer_name":"Bob","order_number":"ORD-5678","complaint_type":"product","severity_level":2,"contact_phone":null}

Now extract from this email (delimiter is """):
"""{{EMAIL}}"""
```

---

🧪 Gatekeeper Test (The One That Matters)

Your pipeline must pass this test email, which intentionally omits the phone number:

```
Hi, my name is Sarah Johnson. My order #ORD-9999 was charged twice on my credit card. It's not super urgent but please fix it.
```

✅ Expected Output (Pass)

```json
{"customer_name":"Sarah Johnson","order_number":"ORD-9999","complaint_type":"billing","severity_level":3,"contact_phone":null}
```

📊 Success Criteria

Criteria Status
Output is only valid JSON ✅
All 5 fields present ✅
Missing phone → null ✅
No conversational filler ✅
Temperature = 0 ✅
Few-shot examples included ✅
Delimiters used properly ✅

---

🧠 Key Learnings

· Few-shot > Zero-shot: Providing 2-3 perfect examples pushes accuracy from ~60% to >99%
· Temperature = 0 makes outputs deterministic
· Delimiters prevent instruction-data conflation (security)
· Null fallback protects downstream systems from silent failures
· Positive framing works better than negative instructions

---

📚 References

· DecodeLabs Prompt Engineering PDF
· Groq API Documentation
· Ollama Documentation
· Min et al. (2022) – "Rethinking the Role of Demonstrations"

---

🙌 Acknowledgements

DecodeLabs – Industrial Training Kit, Batch 2026

---

📬 Contact

· Email: decodelabs.tech@gmail.com
· Location: Greater Lucknow, India
· Website: decodelabs.tech

---

📝 License

This project is for educational purposes as part of the DecodeLabs Industrial Training Program.

---

Happy Prompt Engineering! 🚀
---

🚀 How to Run the Project
