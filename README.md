# MailClear (Django + Fine-Tuned BERT)

A modern, highly accurate Django web application that classifies email text as `spam` or `safe` using a custom fine-tuned BERT-based classifier.

## Features
- **Sleek UI**: Modern glassmorphic dark-mode web forms for validating emails.
- **Custom AI Model**: Uses locally fine-tuned BERT model weights for high accuracy classification.
- **Instant Feedback**: Real-time spam/not-spam predictions along with percentage confidence scores.

## Project Structure

```text
Spam_email_detection/
|-- requirements.txt
|-- train.py                 <-- Fine-tuning script for BERT
|-- fix_reqs.py
|-- fine_tuned_spam_model/   <-- Local directory for your model weights (git-ignored)
|-- spam_detector/
|   |-- manage.py
|   |-- db.sqlite3
|   |-- spam_detector/
|   |   |-- settings.py
|   |   |-- urls.py
|   |   `-- asgi.py
|   `-- classify/
|       |-- spam.py          <-- Model loading & inference logic
|       |-- views.py
|       |-- forms.py
|       |-- urls.py
|       `-- templates/index.html
```

## Local Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Spam_email_detection
```

### 2. Create and activate virtual environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Fine-Tune the Model (Optional)
This repository includes a `train.py` script to generate custom fine-tuned model weights.
```bash
python train.py
```
*Note: This will download datasets and train the model, eventually creating a `fine_tuned_spam_model/` folder. The app will automatically use these local weights if the folder exists, otherwise it will fallback to the un-trained base model.*

### 5. Run migrations
```bash
cd spam_detector
python manage.py migrate
```

### 6. Start development server
```bash
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## How Prediction Works
- The AI inference logic lives in `spam_detector/classify/spam.py`.
- It attempts to load custom weights from `../fine_tuned_spam_model/`.
- If custom weights are unavailable, it defaults to the generic `bert-base-uncased` tokenizer and sequence classifier (`num_labels=2`).
- Returns `spam` or `ham` class with a normalized confidence score display (0-100%).

## Deployment Notes (Render / Railway)

This repo is a Django project inside the `spam_detector/` folder, so configure that as root/workdir on hosting platforms. **Keep in mind you must train or upload your model weights to your host since they are excluded from Git**.

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
