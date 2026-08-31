# Quiz Master - V2

> Modern Application Development - II  
> **IITM BS Degree Program (Diploma in Programming)**


## Overview

Quiz Master - V2 is a multi-user web application designed as an **exam preparation portal** for multiple courses. It includes administrative controls and supports end users (students) who can access quizzes, track progress, and prepare efficiently.


## Tech Stack

| Component        | Framework / Tool     |
|------------------|-----------------------|
| Backend API      | Flask (Python)        |
| Frontend UI      | Vue.js                |
| Database         | SQLite                |
| Caching / Queue  | Redis                 |
| Task Queue       | Celery                |
| Styling          | Bootstrap             |
| Mails            | STMP                  |


## Prerequisites

Before setting up Quiz Master - V2, make sure the following software is installed on your system:

- **Python 3.10+**
- **Node.js 18+** and **npm**
- **Redis**
- **MailHog** (for local email testing)
- **Git**

## Setup Instructions

Follow the steps below to set up and run the application on your local machine.

1. Clone the Repository

```bash
git clone https://github.com/23f2001106/QuizmasterV2.git
cd QuizmasterV2
```

2. Create a `.env` file

Copy `.env.example` to `.env`.

```bash
# On Windows
copy backend\.env.example backend\.env
# On Linux/macOS
cp backend/.env.example backend/.env
```

3. Start Redis

Ensure Redis is installed and running:

```bash
sudo service redis-server start
redis-cli ping   # Should return "PONG"
```

4. Start MailHog

MailHog is used to capture emails locally during development without sending them to real email addresses.

Start MailHog in a separate terminal:

```bash
mailhog
```

By default:

- SMTP Server: `localhost:1025`
- MailHog UI: `http://localhost:8025`

Open the MailHog UI in your browser:

```
http://localhost:8025
```
Keep MailHog running while using the application. 
All emails sent by the application will appear in the MailHog inbox.

5. Setup Backend (Flask)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
python run.py
```

6. Setup the Database

Run the following commands:

```bash
flask db init   # Initialize migrations directory (only required once)
flask db migrate -m "Initial migration"
flask db upgrade
```

7. Run Celery Workers

In separate terminals:

**Worker:**

```bash
cd backend
source venv/bin/activate
celery -A celery_worker.celery worker --loglevel=info
```

**Beat Scheduler:**

```bash
cd backend
source venv/bin/activate
celery -A celery_beat.celery beat --loglevel=info
```

8. Setup Frontend (Vue.js)

In a separate terminal:

```bash
cd frontend
npm install
npm run serve
```

9. Optional: Run Manual Tasks

Run background tasks manually:

```bash
cd backend
python manual_tasks_runner.py
```

### Admin Login Setup

During the first run, an admin account is automatically created.

- Username: `admin@gmail.com`
- Password: (Defaults to `admin123`, unless changed via ADMIN_PASSWORD in .env)