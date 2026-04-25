import os
from twilio.rest import Client

def send_whatsapp(to_number: str, message: str):
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    
    # Debugging: See exactly what the variables look like
    raw_from = os.getenv("TWILIO_WHATSAPP_NUMBER")
    print(f"DEBUG: Raw From from ENV: '{raw_from}'")
    
    # Force the prefix if it's missing
    from_number = raw_from if raw_from.startswith("whatsapp:") else f"whatsapp:{raw_from}"
    formatted_to = to_number if to_number.startswith("whatsapp:") else f"whatsapp:{to_number}"
    
    print(f"DEBUG: Final From: {from_number}")
    print(f"DEBUG: Final To: {formatted_to}")

    try:
        client.messages.create(
            from_=from_number,
            body=message,
            to=formatted_to
        )
        print("✅ Success!")
    except Exception as e:
        print(f"❌ Failed: {e}")