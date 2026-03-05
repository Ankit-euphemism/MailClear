# Spam Email Detection (Django + BERT)

A Django web app that classifies email text as `spam` or `ham` using a BERT-based classifier from Hugging Face Transformers.

## Features
- Web form to paste email content (subject + body)
- Spam/Not-spam prediction with confidence score
- Simple Django UI and routing

## Project Structure

```text
Spam_email_detection/
|-- requirements.txt
|-- spam_detector/
|   |-- manage.py
|   |-- db.sqlite3
|   |-- spam_detector/
|   |   |-- settings.py
|   |   |-- urls.py
|   |   `-- asgi.py
|   `-- classify/
|       |-- spam.py
|       |-- views.py
|       |-- forms.py
|       |-- urls.py
|       `-- templates/index.html
```

## Local Setup

### 1. Clone and enter the repo
```bash
git clone <your-repo-url>
cd Spam_email_detection
```

### 2. Create and activate virtual environment
Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
cd spam_detector
python manage.py migrate
```

### 5. Start development server
```bash
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## How Prediction Works
- Model is loaded in `spam_detector/classify/spam.py`
- Uses `bert-base-uncased` tokenizer and sequence classifier (`num_labels=2`)
- Returns:
  - `label`: `spam` or `ham`
  - `confidence`: probability of predicted class

## Deployment Notes (Render / Railway)

This repo is a Django project inside the `spam_detector/` folder, so configure that as root/workdir on hosting platforms.

### Render
- Root Directory: `spam_detector`
- Build Command:
  ```bash
  pip install -r ../requirements.txt && python manage.py migrate
  ```
- Start Command:
  ```bash
  daphne -b 0.0.0.0 -p 8000 spam_detector.asgi:application
  ```

### Railway
- Root Directory: `spam_detector`
- Build Command (if needed):
  ```bash
  pip install -r ../requirements.txt
  ```
- Start Command:
  ```bash
  daphne -b 0.0.0.0 -p 8000 spam_detector.asgi:application
  ```
- Run once after deploy:
  ```bash
  python manage.py migrate
  ```

## Production Checklist
- Move `SECRET_KEY` out of source code into environment variables
- Configure `ALLOWED_HOSTS` for your deployed domain
- Configure `CSRF_TRUSTED_ORIGINS` for HTTPS domain
- Consider PostgreSQL instead of SQLite for persistent production data
- Ensure host plan has enough RAM/CPU for Transformers + Torch model load
