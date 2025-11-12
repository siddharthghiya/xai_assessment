import streamlit as st
import json
from datetime import datetime

# Assuming database and grok_api are available in the environment
from database import (
    get_all_leads,
    get_leads_count,
    get_lead_by_id,
    update_contacted,
    update_responded,
    update_interested,
    update_meeting_time,
    update_sale_completed,
    increment_follow_up,
    append_message,
    update_status
)
from grok_api import generate_message

st.title("Track Leads")

# --- Initialize Session State for Expander Management ---
if "expanded_state" not in st.session_state:
    st.session_state["expanded_state"] = {}

# --- Pagination and Search Setup ---
search = st.text_input("Search leads by name, company, or email")
total_count = get_leads_count(search)
page_size = 10
total_pages = max((total_count + page_size - 1) // page_size, 1)

page = st.selectbox(
    "Page",
    options=range(1, total_pages + 1),
    index=0,
    key="page"
)
offset = (page - 1) * page_size

# --- Lead Count Info ---
if search and total_count == 0:
    st.info(f"No leads found matching '{search}'.")
elif total_count == 0:
    st.info("No leads yet. Add some leads first.")
else:
    st.info(
        f"Showing {min(page_size, total_count - offset)} of {total_count} leads "
        f"(Page {page} of {total_pages})"
    )

# --- Fetch Leads ---
leads = get_all_leads(search=search, limit=page_size, offset=offset)

# --- Lead Display Loop ---
for lead in leads:
    (
        lead_id, name, company, email, description, score, message, status,
        contacted, responded, interested, meeting_time, sale_completed,
        follow_up_count, sent_messages, *extra
    ) = lead

    expander_key = f"expander_{lead_id}"
    if expander_key not in st.session_state["expanded_state"]:
        st.session_state["expanded_state"][expander_key] = False

    with st.expander(
        f"**{name}** - {company} (Score: {score}) - Status: {status}",
        expanded=st.session_state["expanded_state"][expander_key]
    ):
        st.write(f"Email: {email}")
        st.write(f"Description: {description}")
        st.write(f"Follow-up Count: {follow_up_count}")

        # --- Message History ---
        st.subheader("Message History")

        if sent_messages and sent_messages.strip():
            try:
                messages_list = json.loads(sent_messages)
            except json.JSONDecodeError:
                st.error("Error parsing message history. Data may be corrupt.")
                messages_list = []
        else:
            messages_list = []

        if messages_list:
            # Initial message
            st.markdown("##### 💬 Initial Outreach")
            with st.chat_message("assistant", avatar="📧"):
                st.markdown(messages_list[0].strip())

            # Follow-ups
            if len(messages_list) > 1:
                follow_ups = messages_list[1:]
                with st.expander(f"View {len(follow_ups)} Follow-up(s)"):
                    for i, msg in enumerate(follow_ups):
                        with st.chat_message("assistant", avatar="🔄"):
                            st.caption(f"Follow-up #{i + 1}")
                            st.markdown(msg.strip())
        else:
            st.write("No messages sent yet.")

        # --- Progress visualization ---
        status_to_progress = {
            "New": 0,
            "Contacted": 1,
            "Follow-up Sent": 1,
            "Responded": 2,
            "Not Interested": 2,
            "Interested": 3,
            "Meeting Scheduled": 4,
            "Sale Not Made": 4,
            "Sale Completed": 5
        }
        progress_value = status_to_progress.get(status, 0) / 5
        st.progress(progress_value)
        st.markdown(f"Progress: **{status}**")
        st.markdown("---")

        # --- Interaction Logic ---
        # 1. Initial Contact
        if not contacted:
            st.subheader("Lead not contacted yet.")
            draft_shown_key = f"draft_shown_{lead_id}"
            if draft_shown_key not in st.session_state:
                st.session_state[draft_shown_key] = False

            if st.button(f"Draft Initial Message for {name}", key=f"draft_btn_{lead_id}"):
                lead_data = f"Name: {name}, Company: {company}, Email: {email}, Description: {description}"
                st.session_state[f"draft_{lead_id}"] = generate_message(lead_data)
                st.session_state[draft_shown_key] = True
                st.session_state["expanded_state"][expander_key] = True
                st.rerun()

            if st.session_state[draft_shown_key]:
                draft = st.session_state[f"draft_{lead_id}"]
                st.text_area(
                    "Draft Message (copy and send manually)",
                    value=draft,
                    height=150,
                    key=f"draft_text_{lead_id}"
                )

                if st.button("Confirm Message Sent", key=f"confirm_sent_{lead_id}"):
                    append_message(lead_id, draft)
                    update_contacted(lead_id, True)
                    update_status(lead_id, "Contacted")
                    st.session_state[draft_shown_key] = False
                    st.success("Message confirmed sent and status updated! 📧")
                    st.session_state["expanded_state"][expander_key] = True
                    st.rerun()

        # 2. Response and Follow-up
        elif not responded:
            st.subheader("Lead contacted. Has the lead responded?")
            response = st.radio(
                "Has the lead responded?",
                ["Awaiting Response", "No (Send Follow-up)", "Yes"],
                index=0,
                key=f"response_{lead_id}"
            )

            if response == "No (Send Follow-up)":
                followup_shown_key = f"followup_shown_{lead_id}"
                if followup_shown_key not in st.session_state:
                    st.session_state[followup_shown_key] = False

                if st.button(f"Draft Follow-up for {name}", key=f"followup_draft_{lead_id}"):
                    lead_data = f"Name: {name}, Company: {company}, Email: {email}, Description: {description}"
                    st.session_state[f"followup_{lead_id}"] = generate_message(lead_data, is_follow_up=True, follow_up_number=follow_up_count + 1)
                    st.session_state[followup_shown_key] = True
                    st.session_state["expanded_state"][expander_key] = True
                    st.rerun()

                if st.session_state[followup_shown_key]:
                    followup_draft = st.session_state[f"followup_{lead_id}"]
                    st.text_area(
                        "Follow-up Draft (copy and send manually)",
                        value=followup_draft,
                        height=150,
                        key=f"followup_text_{lead_id}"
                    )

                    if st.button("Confirm Follow-up Sent", key=f"confirm_followup_{lead_id}"):
                        append_message(lead_id, followup_draft)
                        increment_follow_up(lead_id)
                        update_status(lead_id, "Follow-up Sent")
                        st.session_state[followup_shown_key] = False
                        st.success("Follow-up confirmed sent! 📩")
                        st.session_state["expanded_state"][expander_key] = True
                        st.rerun()

            elif response == "Yes":
                if st.button("Confirm Lead Responded", key=f"confirm_responded_{lead_id}"):
                    update_responded(lead_id, True)
                    update_status(lead_id, "Responded")
                    st.success("Lead response confirmed! 📞")
                    st.session_state["expanded_state"][expander_key] = True
                    st.rerun()

        # 3. Qualification (Interested/Not Interested)
        elif interested is None:
            st.subheader("Lead responded. Is the lead interested?")
            interest = st.radio("Is the lead interested?", ["Yes", "No"], key=f"interest_{lead_id}")

            if interest == "No":
                if st.button("Confirm Not Interested", key=f"confirm_not_interested_{lead_id}"):
                    update_interested(lead_id, False)
                    update_status(lead_id, "Not Interested")
                    st.success("Status updated to Not Interested. 🚫")
                    st.session_state["expanded_state"][expander_key] = True
                    st.rerun()

            elif interest == "Yes":
                if st.button("Confirm Interested", key=f"confirm_interested_{lead_id}"):
                    update_interested(lead_id, True)
                    update_status(lead_id, "Interested")
                    st.success("Lead interest confirmed! 👍")
                    st.session_state["expanded_state"][expander_key] = True
                    st.rerun()

        # 4. Meeting Scheduling
        elif interested and meeting_time is None:
            st.subheader("Lead is interested. Schedule a meeting.")

            col1, col2 = st.columns(2)
            with col1:
                meeting_date_input = st.date_input("Meeting Date", key=f"meeting_date_{lead_id}")
            with col2:
                meeting_time_input = st.time_input("Meeting Time", key=f"meeting_time_{lead_id}")

            full_time = datetime.combine(meeting_date_input, meeting_time_input).isoformat()

            if st.button("Confirm Meeting Scheduled", key=f"confirm_schedule_{lead_id}"):
                update_meeting_time(lead_id, full_time)
                update_status(lead_id, "Meeting Scheduled")
                st.success(f"Meeting confirmed for **{full_time}**! 🗓️")
                st.session_state["expanded_state"][expander_key] = True
                st.rerun()

        # 5. Sale Outcome
        elif not sale_completed:
            st.subheader("Meeting scheduled. Was the sale made?")
            sale_outcome = st.radio("Was the sale made?", ["Yes", "No"], key=f"sale_outcome_{lead_id}")

            if sale_outcome == "No":
                if st.button("Confirm Sale Not Made", key=f"confirm_sale_not_made_{lead_id}"):
                    update_status(lead_id, "Sale Not Made")
                    st.success("Status updated to Sale Not Made. 🙁")
                    st.session_state["expanded_state"][expander_key] = True
                    st.rerun()

            elif sale_outcome == "Yes":
                if st.button("Confirm Sale Completed", key=f"confirm_sale_completed_{lead_id}"):
                    update_sale_completed(lead_id, True)
                    update_status(lead_id, "Sale Completed")
                    st.success("Status updated to Sale Completed! 💰")
                    st.session_state["expanded_state"][expander_key] = True
                    st.rerun()

        # 6. Final State
        else:
            st.success("Sale Completed! 🎉")
