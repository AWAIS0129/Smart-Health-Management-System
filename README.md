# Smart Health Management System

A web app that helps you track and manage your health parameters in one place — log your vitals, visualize trends, get AI-powered insights, and receive health notifications.

## Features

- 🩺 **Health Tracking** — log weight, blood pressure, pulse, blood sugar, temperature, sleep time, exercise duration, and stress level over time
- 📊 **Data Visualization** — view your health data as charts and trends on a personal dashboard
- 🤖 **AI Insights** — get AI-driven inferences based on your health history
- 📄 **Reports** — generate health reports
- 🔔 **Notifications** — stay updated with alerts about your health
- 👤 **User Accounts** — secure sign-up/login with personal health profiles

## Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite
- **Frontend:** Tailwind CSS + Chart.js

## How to Use

**1. Clone the repo**
```bash
git clone https://github.com/AWAIS0129/Smart-Health-Management-System.git
cd Smart-Health-Management-System
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
npm install
```

**3. Set up environment variables**

Copy `.env.example` to `.env` in the root folder and add your own `SECRET_KEY`:
```bash
cp .env.example .env
```

**4. Start Tailwind (in its own terminal)**
```bash
npm run watch:css
```

**5. Run migrations & start the server**
```bash
cd smart_health_management_system
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser 🎉
