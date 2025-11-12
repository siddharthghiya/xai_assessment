from grok_api import rank_lead, generate_message

# Dummy data
lead_data = "Name: John Doe, Company: Tech Corp, Email: john@tech.com, Description: Interested in AI tools"
ranking_desc = "Prefer leads in tech industry with large teams"

try:
    score = rank_lead(lead_data, ranking_desc)
    print(f"Score: {score}")
except Exception as e:
    print(f"Error: {e}")

try:
    message = generate_message(lead_data)
    print(f"Message: {message}")
except Exception as e:
    print(f"Error: {e}")
