import sqlite3
from database import insert_lead

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

# Verify by querying
conn = sqlite3.connect('leads.db')
cursor = conn.cursor()
cursor.execute('SELECT name, email, gender, age, profession, industry, income_level, location, interests, preferred_contact, pain_points FROM leads WHERE id = ?', (lead_id,))
row = cursor.fetchone()
conn.close()

print(f"Inserted lead ID: {lead_id}")
print("Verified data:", row)
