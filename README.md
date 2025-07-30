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


## Setup Instructions

Follow the steps below to set up and run the application on your local machine.

### 1. Clone the Repository

```
git clone https://github.com/23f2001106/MAD-2-Project.git.git
cd MAD-2-Project
```

### 2. Start Redis

Ensure Redis is installed and running:

```sudo service redis-server start
redis-cli ping   # Should return "PONG"
```

### 3. Setup Backend (Flask)

```cd backend
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
python run.py
```

### 4. Setup the Database

Run the following commands:

```
flask db init   # Initialize migrations directory (only required once)
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Run Celery Workers

In separate terminals:

**Worker:**

bash
```cd backend
source venv/bin/activate
celery -A celery_worker.celery worker --loglevel=info
```

**Beat Scheduler:**

```
cd backend
source venv/bin/activate
celery -A celery_beat.celery beat --loglevel=info
```

### 6. Setup Frontend (Vue.js)

```cd frontend
npm install
npm run serve
```

### 7. Optional: Run Manual Tasks

Run background tasks manually:

```
cd backend
python manual_tasks_runner.py
```


To view mails use `Mailhog UI`

### Admin Login Setup

During the first run, an admin account is automatically created.

- Username: `admin@gmail.com`
- Password: (Defaults to `admin123`, unless changed via ADMIN_PASSWORD in .env)