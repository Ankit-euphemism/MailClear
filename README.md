# MailClear

MailClear is a Django web application that classifies submitted email or message text as `spam` or `ham` (legitimate). It uses a BERT sequence-classification model and displays the predicted label with its confidence score in a simple web interface.

## Project Description in Details

MailClear provides an accessible way to screen suspicious email content before a user interacts with it. The Django application accepts message text through a browser form, tokenizes it with a BERT tokenizer, and runs it through a two-class Transformer model. The result page reports whether the text is likely spam or ham, together with a normalized confidence percentage.

The project includes both the web application and a model-training workflow. `train.py` fine-tunes `bert-base-uncased` on the UCI SMS Spam Collection dataset, evaluates the model using accuracy, precision, recall, and F1 score, and saves the resulting model files locally. At runtime, the application loads those fine-tuned weights when available; otherwise, it falls back to the base BERT model.

## Key Features and Technologies

- **Spam classification:** Predicts `spam` or `ham` from user-provided email/message text.
- **Confidence score:** Displays the model probability for the predicted class as a percentage.
- **Fine-tuning workflow:** Includes a reproducible training script using the UCI SMS Spam Collection dataset.
- **Local model support:** Automatically loads model weights from `fine_tuned_spam_model/` when they have been trained or supplied.
- **Web interface:** Django form handling and templates provide a straightforward browser-based experience.
- **Technologies:** Python, Django, PyTorch, Hugging Face Transformers, Hugging Face Datasets, scikit-learn, and Daphne (ASGI server).

## Problem Statement and Proposed Solution

Unsolicited and deceptive messages can expose users to phishing, fraud, and unwanted content. Manually deciding whether every unfamiliar message is trustworthy is time-consuming and inconsistent, especially when messages use persuasive language or misleading offers.

MailClear addresses this by applying natural-language processing to the text of a message. A BERT-based classifier learns patterns associated with spam and legitimate messages from labeled examples, then provides an immediate prediction and confidence score through a Django web app. This gives users a quick initial screening tool while keeping the model-training and deployment workflow contained in one project.

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
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### Run locally with the launcher scripts

After creating the virtual environment and installing dependencies, run the launcher from the project root. Each launcher activates the environment, optionally trains the model, and starts the Django development server.

**Windows (PowerShell or Command Prompt):**
```powershell
.\run_project.bat
```

**macOS/Linux (Terminal):**
```bash
chmod +x run_project.sh
./run_project.sh
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
