# 🏥 School Health Chatbot - Science Fair Project

An AI-powered health chatbot that generates personalized health reports for students using Google Gemini API.

## 🌟 Features

- **Health Assessment**: Calculate BMI and health score
- **Personalized Diet Plans**: Vegetarian meal suggestions
- **Exercise Recommendations**: Age-appropriate physical activities
- **Yoga Guidance**: Simple yoga poses with benefits
- **Bilingual Support**: English and Gujarati languages
- **Kid-Friendly Interface**: Colorful, engaging design

---

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))
- Modern web browser

---

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project

Download all files and organize them in the following structure:

```
health-chatbot/
├── backend/
│   ├── app.py
│   ├── gemini_service.py
│   ├── config.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── .env
└── README.md
```

### Step 2: Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key"
4. Copy your API key

### Step 3: Configure Environment Variables

1. Create a file named `.env` in the root directory
2. Add your API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
SECRET_KEY=any_random_secret_key_123
DEBUG=True
```

### Step 4: Install Python Dependencies

Open terminal/command prompt in the `backend` folder and run:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install flask flask-cors python-dotenv google-generativeai