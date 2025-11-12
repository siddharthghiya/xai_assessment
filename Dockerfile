FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["sh", "-c", "python populate_tmp_leads.py && streamlit run app.py --server.port=8501"]
