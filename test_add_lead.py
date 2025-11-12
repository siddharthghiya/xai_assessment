from database import insert_lead, update_score, update_message, update_status, get_ranking_desc
from grok_api import rank_lead, generate_message

# Sample data
name = "Test User"
email = "test@example.com"
gender = "Male"
age = 35
profession = "Software Engineer"
industry = "Tech"
income_level = "High"
location = "San Francisco, USA"
interests = "AI, Programming"
preferred_contact = "Email"
pain_points = "Needs better productivity tools"

lead_id = insert_lead(name, email, gender, age, profession, industry, income_level, location, interests, preferred_contact, pain_points)
update_status(lead_id, "New")

ranking_desc = get_ranking_desc()
lead_data = f"Name: {name}, Email: {email}, Gender: {gender}, Age: {age}, Profession: {profession}, Industry: {industry}, Income Level: {income_level}, Location: {location}, Interests: {interests}, Preferred Contact: {preferred_contact}, Pain Points: {pain_points}"

score = rank_lead(lead_data, ranking_desc) if ranking_desc else 0
update_score(lead_id, score)
update_status(lead_id, "Qualified")

message = generate_message(lead_data)
update_message(lead_id, message)
update_status(lead_id, "Outreach Generated")

print(f"Test lead added: ID {lead_id}, Score: {score}")
