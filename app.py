# app.py — Phishing Email Detection Web App

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import joblib

# Load model and vectorizer
model = joblib.load("phishing_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Initialize FastAPI app
app = FastAPI(title="Phishing Email Detection System")

# Home route
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Phishing Email Detector</title>
            <style>
                body {font-family: Arial, sans-serif; background-color: #f5f6fa; text-align: center; margin-top: 50px;}
                textarea {width: 60%; height: 150px; padding: 10px; font-size: 16px; border-radius: 8px; border: 1px solid #ccc;}
                button {margin-top: 20px; padding: 10px 30px; font-size: 18px; border: none; border-radius: 8px; background-color: #0984e3; color: white; cursor: pointer;}
                button:hover {background-color: #74b9ff;}
                .result {margin-top: 30px; font-size: 22px; font-weight: bold;}
            </style>
        </head>
        <body>
            <h1>📧 Phishing Email Detection System</h1>
            <form action="/predict/" method="post">
                <textarea name="content" placeholder="Paste your email text here..."></textarea><br>
                <button type="submit">Detect</button>
            </form>
        </body>
    </html>
    """

# Prediction route
@app.post("/predict/", response_class=HTMLResponse)
def predict(content: str = Form(...)):
    clean_text = content.lower()
    vectorized = vectorizer.transform([clean_text])
    prediction = model.predict(vectorized)[0]

    result = "🚨 Phishing / Spam Email" if prediction == 1 else "✅ Legitimate Email"

    return f"""
    <html>
        <head>
            <title>Phishing Detection Result</title>
            <style>
                body {{font-family: Arial, sans-serif; background-color: #f1f2f6; text-align: center; margin-top: 50px;}}
                .result {{font-size: 24px; font-weight: bold; margin-top: 30px;}}
                a {{display: inline-block; margin-top: 30px; text-decoration: none; color: #0984e3; font-size: 18px;}}
            </style>
        </head>
        <body>
            <h1>📧 Phishing Email Detection System</h1>
            <div class="result">{result}</div>
            <a href="/">🔙 Try Another Email</a>
        </body>
    </html>
    """
