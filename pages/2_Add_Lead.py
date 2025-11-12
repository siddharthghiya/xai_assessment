import streamlit as st
from database import insert_lead, update_score, update_message, update_status, get_ranking_desc
from grok_api import rank_lead, generate_message

st.title("Add New Lead")

with st.form("new_lead"):
    name = st.text_input("Name", key="name")
    email = st.text_input("Email", key="email")
    gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"], key="gender")
    age = st.number_input("Age", min_value=0, max_value=120, value=30, key="age")
    profession = st.text_input("Profession", key="profession")
    is_working = st.checkbox("Currently Working?", key="is_working")
    industry = None
    if is_working:
        industry = st.text_input("Industry (if working)", key="industry")
    income_level = st.selectbox("Income Level (optional)", ["", "Low", "Medium", "High", "Prefer not to say"], index=0, key="income_level")
    location = st.text_input("Location (City/Country)", key="location")
    preferred_contact = st.selectbox("Preferred Contact Method", ["Email", "Phone", "SMS"], key="preferred_contact")
    submit = st.form_submit_button("Add and Process Lead")

if submit:
    industry_val = industry if is_working else None
    income_level_val = income_level if income_level else None
    if name and email:
        try:
            lead_id = insert_lead(name, email, gender, age, profession, industry_val, income_level_val, location, preferred_contact)
            update_status(lead_id, "New")
            
            ranking_desc = get_ranking_desc()
            lead_data = f"Name: {name}, Email: {email}, Gender: {gender}, Age: {age}, Profession: {profession}, Industry: {industry_val or 'N/A'}, Income Level: {income_level_val or 'N/A'}, Location: {location or 'N/A'}, Interests: {interests or 'N/A'}, Preferred Contact: {preferred_contact}, Pain Points: {pain_points or 'N/A'}"
            
            # Rank
            score = rank_lead(lead_data, ranking_desc) if ranking_desc else 0
            update_score(lead_id, score)
            update_status(lead_id, "Qualified")
            
            # Generate message
            message = generate_message(lead_data)
            update_message(lead_id, message)
            update_status(lead_id, "Outreach Generated")
            
            st.success(f"Lead added successfully! ID: {lead_id}, Score: {score}")
        except Exception as e:
            st.error(f"Error processing lead: {str(e)}")
    else:
        st.error("Please fill in name and email.")
