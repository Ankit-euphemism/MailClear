from transformers import BertTokenizer, BertForSequenceClassification
import torch
import os

# Define path to the fine-tuned model in the root directory
# __file__ is inside spam_detector/classify/spam.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FINE_TUNED_MODEL_PATH = os.path.join(BASE_DIR, 'fine_tuned_spam_model')

# Check if fine-tuned model exists, otherwise fallback to base model
if os.path.exists(FINE_TUNED_MODEL_PATH) and os.path.isdir(FINE_TUNED_MODEL_PATH):
    print("✅ Loading fine-tuned spam model from local directory...")
    MODEL_NAME = FINE_TUNED_MODEL_PATH
else:
    print("⚠️ Fine-tuned model not found. Falling back to the untrained base model...")
    MODEL_NAME = 'bert-base-uncased'

tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def predict_spam(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {key: val.to(device) for key, val in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=1)
        predicted_class = torch.argmax(logits, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
    return {
        "label": "spam" if predicted_class == 1 else "ham",
        "confidence": confidence
    }