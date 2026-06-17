# main.py
from extract import extract_ticket
import json

def main():
    print("Loading raw email...")
    with open('raw_data.txt', 'r') as file:
        messy_email = file.read()
    
    print("Sending to Ollama (temp=0, json mode)...")
    # Run the extraction
    result = extract_ticket(messy_email)
    
    print("\n--- SUCCESS ---")
    print("Validated Pydantic Object:")
    print(result)
    
    print("\n--- RAW JSON OUTPUT ---")
    # The .model_dump_json() gives us the perfect string
    print(result.model_dump_json(indent=2))
    
    # The Gatekeeper Test: Check if phone is null
    if result.contact_phone is None:
        print("\n✓ GATEKEEPER TEST PASSED: Phone number is correctly NULL.")
    else:
        print(f"\n✗ GATEKEEPER TEST FAILED: Hallucinated a phone number: {result.contact_phone}")

if __name__ == "__main__":
    main()