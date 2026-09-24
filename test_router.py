# test_router.py
from dotenv import load_dotenv
load_dotenv()

import jevlang
import triage

test_tickets = [
    "I was charged twice for my subscription. I need a refund immediately!",
    "The app keeps crashing every time I try to upload a photo.",
    "How do I reset my password? I can't log in.",
    "I'm not sure what's wrong, it just doesn't work.",
]

for ticket in test_tickets:
    print(f"\n--- Ticket: {ticket[:50]}... ---")
    result = triage.analyze_ticket(ticket)

    # Choice → str subclass. The label IS the string value.
    dept_label = str(result.department)
    dept_conf = result.department.confidence
    print(f"  Department: {dept_label} (confidence: {dept_conf:.2f})")

    # Score → float subclass. Use it directly as a number.
    urgency_score = float(result.urgency)
    print(f"  Urgency: {urgency_score:.2f}")

    # Noul → float subclass. Probability 0.0 to 1.0.
    angry_prob = float(result.is_angry)
    print(f"  Angry: {angry_prob:.2f}")

    # Noul is truthy at >= 0.5
    if result.is_angry:
        print("  (customer is upset)")