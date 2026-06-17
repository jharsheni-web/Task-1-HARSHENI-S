# src/extractor.py
import os
import json
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
import ollama

# This IS the 'Five-Variable Gatekeeper Protocol' from the PDF (Page 19)
class SupportTicket(BaseModel):
    customer_name: str = Field(description="The full name of the customer")
    order_number: str = Field(description="The order number starting with #")
    complaint_type: str = Field(description="Type of issue: Damaged, Late, Wrong Item, or Billing")
    severity_level: int = Field(ge=1, le=5, description="Urgency from 1 (Low) to 5 (Critical)")
    contact_phone: Optional[str] = None # Explicitly allows NULL as per PDF Page 11

# src/extractor.py (continued)

SYSTEM_PROMPT = """You are a deterministic data extraction engine. You do NOT chat.
You do NOT add explanations. You output ONLY valid JSON.
Follow the schema exactly. If data is missing, use null.
--- SCHEMA ---
{
    "customer_name": "string",
    "order_number": "string",
    "complaint_type": "Damaged | Late | Wrong Item | Billing",
    "severity_level": "integer 1-5",
    "contact_phone": "string or null"
}
--- FEW-SHOT EXAMPLES ---
### INPUT:
User Emma Jones says order #A999 is 3 weeks late. No phone given.
### OUTPUT:
{"customer_name": "Emma Jones", "order_number": "#A999", "complaint_type": "Late", "severity_level": 4, "contact_phone": null}
### INPUT:
Order #B123 for Mike R. Wrong item received. Call 555-1234.
### OUTPUT:
{"customer_name": "Mike R.", "order_number": "#B123", "complaint_type": "Wrong Item", "severity_level": 3, "contact_phone": "555-1234"}
"""

def extract_ticket(raw_text: str) -> SupportTicket:
    # 1. Use delimiters (""") to separate instruction from data (PDF Page 7)
    # 2. Append the raw text at the end
    user_prompt = f"""Extract data from the text below:
    \"\"\"{raw_text}\"\"\"
    """
    
    try:
        # 3. Force deterministic behavior
        response = ollama.chat(
            model='llama3.2:1b',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_prompt}
            ],
            format='json', # CRITICAL: Bans conversational filler (PDF Page 10) [citation:2]
            options={
                'temperature': 0, # Kills creativity (PDF Page 8) [citation:1][citation:10]
                'seed': 42       # Ensures reproducibility
            }
        )
        
        # 4. Parse the raw string output into our Pydantic class
        ticket = SupportTicket.model_validate_json(response['message']['content'])
        return ticket
        
    except (json.JSONDecodeError, ValidationError) as e:
        # This is the "Repair Loop" logic from PDF Page 18
        print(f"Error parsing response: {e}")
        print(f"Raw output was: {response['message']['content']}")
        # In production, you'd send this error back to the LLM here
        raise Exception("Failed to extract data deterministically")