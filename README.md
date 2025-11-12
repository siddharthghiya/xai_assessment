# Grok-Powered SDR Prototype

## Overview
This is a simple prototype for a Grok-powered Sales Development Representative (SDR) system. It focuses on core features: adding a new lead, storing it in a database, qualifying/scoring the lead using Grok API, generating a personalized outreach message, and tracking progress through basic pipeline stages (New → Qualified → Outreach Generated).

### Features
- **Lead Input**: User-friendly form to input lead details (name, company, email, description) and qualification criteria.
- **Data Storage**: Uses SQLite for CRUD operations to store leads, scores, messages, and status.
- **Grok Integration**: Calls Grok API to score leads based on criteria (1-10) and generate personalized messages. Includes error handling and response validation.
- **Progress Tracking**: Displays all leads with their status, score, and generated message.
- **User Experience**: Built with Streamlit for an intuitive Python-based web interface.

### Technical Architecture
- **Backend**: Python with SQLite for database (database.py), requests for API calls (grok_api.py).
- **Frontend**: Streamlit (app.py) for the UI.
- **API Integration**: Assumes Grok API endpoint similar to OpenAI's. Prompts are engineered for qualification and messaging. API key loaded from .env.
- **Error Handling**: Checks for API key, handles request errors, validates responses.

### Local Setup Instructions
1. Clone the repository or copy the files.
2. Install dependencies: `pip install -r requirements.py`
3. Add your Grok API key to `.env`: `GROK_API_KEY=your_key_here`
4. Run the app: `streamlit run app.py`
5. Access the app at `http://localhost:8501`
6. Navigate using the sidebar to:
  - **Ranking Description**: Update the ranking description for lead scoring.
  - **Add Lead**: Add new leads and auto-process (rank, generate message).
  - **Track Leads**: View up to 10 leads, click expanders for details, progress, messages, and interactive updates (contact, follow-up, meeting, sale).

### Containerized Deployment
1. Ensure Docker and Docker Compose are installed.
2. Build and run: `docker-compose up --build`
3. Access the app at `http://localhost:8501`
4. **Note**: When the Docker container is first created and started, the system automatically populates the database with some random temporary leads for demonstration purposes. These are generated via the `populate_tmp_leads.py` script.
5. Note: Set GROK_API_KEY in your environment or .env before building.

### Troubleshooting
- **API Errors**: Ensure GROK_API_KEY is set and valid in .env. The call uses 'grok-4-latest' model with system/user messages, stream=False, temperature=0. Check endpoint in grok_api.py if different.
- **Database Issues**: leads.db is created automatically. Delete it to reset.
- **Streamlit Not Running**: Verify port 8501 is free.
- **Dependencies**: If pip install fails, check Python version (3.9+ recommended).

### Usage
- **Update Ranking Criteria**: Navigate to the "Ranking Description" page in the sidebar. Enter or update the ranking description in the text area, then click "Update Ranking Description". This will save the new criteria and automatically re-score and re-rank all existing leads based on the updated description.
- **Add a New Lead**: Go to the "Add Lead" page. Fill in the lead details (name, company, email, description) and submit the form. The system will automatically score the lead using Grok API based on the current ranking criteria and generate a personalized outreach message.
- **Track Leads Workflow**: Navigate to the "Track Leads" page to manage and progress leads through the pipeline:
  - Search for leads by name, company, or email, with pagination to browse results.
  - Expand individual lead entries to view details (email, description, score, status, follow-up count, message history).
  - Interact with leads based on their current status:
    - If not contacted: Draft and confirm sending an initial outreach message.
    - If contacted but no response: Draft and confirm sending follow-up messages.
    - Update response status (responded or not).
    - Mark interest level (interested or not).
    - Record sale outcomes (completed or not).
  - View progress bars and message histories for each lead.

This prototype is minimal for demo purposes. Expand as needed for full features like advanced evals or search.
