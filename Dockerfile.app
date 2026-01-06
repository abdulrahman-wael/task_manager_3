FROM python:3.11-slim

WORKDIR /app
COPY frontend_requirements.txt .
RUN pip install --no-cache-dir -r frontend_requirements.txt
EXPOSE 8501

COPY app.py .
CMD streamlit run app.py