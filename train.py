import os
import torch
from datasets import load_dataset
from dotenv import load_dotenv
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Load local configuration without committing secrets.
load_dotenv()

# 1. Configuration
MODEL_NAME = 'bert-base-uncased'
OUTPUT_DIR = './fine_tuned_spam_model'
EPOCHS = 3
BATCH_SIZE = 8
HF_TOKEN = os.getenv('HF_TOKEN')

# Check if CUDA is available for GPU training
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(f"Using device: {device}")

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def main():
    print("Loading SMS Spam dataset...")
    # Use the canonical namespace-qualified repository ID.
    dataset = load_dataset("ucirvine/sms_spam", token=HF_TOKEN)
    
    # The dataset has a 'train' split which we can split further
    dataset = dataset['train'].train_test_split(test_size=0.2, seed=42)
    train_dataset = dataset['train']
    test_dataset = dataset['test']
    
    print("Loading Tokenizer...")
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME, token=HF_TOKEN)
    
    def tokenize_function(examples):
        # sms_spam has features: 'sms' (text) and 'label' (0 or 1)
        # Note: label 1 is usually spam, 0 is ham in sms_spam dataset
        return tokenizer(examples["sms"], padding="max_length", truncation=True, max_length=512)

    print("Tokenizing datasets...")
    tokenized_train = train_dataset.map(tokenize_function, batched=True)
    tokenized_test = test_dataset.map(tokenize_function, batched=True)
    
    # Rename columns to match what Trainer expects
    tokenized_train = tokenized_train.rename_column("label", "labels")
    tokenized_test = tokenized_test.rename_column("label", "labels")
    tokenized_train.set_format("torch", columns=["input_ids", "attention_mask", "labels"])
    tokenized_test.set_format("torch", columns=["input_ids", "attention_mask", "labels"])
    
    print("Loading Model...")
    model = BertForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
        token=HF_TOKEN,
    )
    model.to(device)
    
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        warmup_steps=500,
        weight_decay=0.01,
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        dataloader_pin_memory=torch.cuda.is_available(),
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_test,
        compute_metrics=compute_metrics,
    )
    
    print("Starting training...")
    trainer.train()
    
    print("Evaluating model...")
    eval_results = trainer.evaluate()
    print(f"Evaluation Results: {eval_results}")
    
    print(f"Saving fine-tuned model to {OUTPUT_DIR}...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Training complete! You can now update your Django app to use the new local model.")

if __name__ == "__main__":
    main()
