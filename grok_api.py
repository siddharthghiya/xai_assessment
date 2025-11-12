import os
import requests
from dotenv import load_dotenv
from config import PRODUCT_DESCRIPTION

load_dotenv()

GROK_API_KEY = os.getenv('GROK_API_KEY')
GROK_API_URL = 'https://api.x.ai/v1/chat/completions'  # Assumed endpoint; adjust if different

def call_grok(messages, max_tokens=500):
    if not GROK_API_KEY:
        raise ValueError("GROK_API_KEY is not set in .env file")

    headers = {
        'Authorization': f'Bearer {GROK_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'grok-4-fast-reasoning',
        'messages': messages,
        'max_tokens': max_tokens,
        'stream': False,
        'temperature': 0
    }
    try:
        response = requests.post(GROK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content'].strip()
        else:
            raise ValueError("Invalid response from Grok API")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Grok API error: {str(e)}")

def rank_lead(lead_data, ranking_desc):
    messages = [
        {"role": "system", "content": f"You are a sales ranking expert. Product description: {PRODUCT_DESCRIPTION}"},
        {"role": "user", "content": f"Lead details: {lead_data}\nRanking description: {ranking_desc}\nRank this lead on a scale of 1-10, where 10 is highly preferred based on the ranking description and product fit. Provide only the score as an integer."}
    ]
    response = call_grok(messages, max_tokens=10)
    try:
        return int(response)
    except ValueError:
        raise ValueError("Invalid score from Grok")

def generate_message(lead_data, is_follow_up=False, follow_up_number=None):
    if is_follow_up:
        if follow_up_number is None:
            user_content = f"This is a follow-up message. Lead details: {lead_data}\nCreate a follow-up outreach message. Make it professional, engaging, reference previous contact, tailored to their company and description, and highlight product fit. Keep it under 200 words."
        elif follow_up_number == 1:
            user_content = f"This is the first follow-up. Reference the initial contact and gently remind them of our previous conversation. Lead details: {lead_data}\nCreate a follow-up outreach message. Make it professional, engaging, tailored to their company and description, and highlight product fit. Keep it under 200 words."
        elif follow_up_number == 2:
            user_content = f"This is the second follow-up. Offer additional value or insights related to their needs. Lead details: {lead_data}\nCreate a follow-up outreach message. Make it professional, engaging, reference previous contact, tailored to their company and description, and highlight product fit. Keep it under 200 words."
        elif follow_up_number == 3:
            user_content = f"This is the final follow-up. Reach out one last time to check in and see if there's any interest. Lead details: {lead_data}\nCreate a follow-up outreach message. Make it professional, engaging, reference previous contact, tailored to their company and description, and highlight product fit. Keep it under 200 words."
        else:
            user_content = f"This is an additional follow-up. Lead details: {lead_data}\nCreate a follow-up outreach message. Make it professional, engaging, reference previous contact, tailored to their company and description, and highlight product fit. Keep it under 200 words."
    else:
        user_content = f"Create a personalized outreach message for this lead: {lead_data}\nMake it professional, engaging, tailored to their company and description, and highlight product fit. Keep it under 200 words."
    messages = [
        {"role": "system", "content": f"You are a sales outreach specialist. Product description: {PRODUCT_DESCRIPTION}"},
        {"role": "user", "content": user_content}
    ]
    return call_grok(messages)
