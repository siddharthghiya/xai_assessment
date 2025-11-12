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
4. Note: Set GROK_API_KEY in your environment or .env before building.

### Troubleshooting
- **API Errors**: Ensure GROK_API_KEY is set and valid in .env. The call uses 'grok-4-latest' model with system/user messages, stream=False, temperature=0. Check endpoint in grok_api.py if different.
- **Database Issues**: leads.db is created automatically. Delete it to reset.
- **Streamlit Not Running**: Verify port 8501 is free.
- **Dependencies**: If pip install fails, check Python version (3.9+ recommended).

### Usage
- Fill in the form and submit to add/process a lead.
- View processed leads below the form.

This prototype is minimal for demo purposes. Expand as needed for full features like advanced evals or search.
