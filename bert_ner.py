import os
import json
import glob
import torch
from torch.utils.data import Dataset
from transformers import BertTokenizerFast, BertForTokenClassification, Trainer, TrainingArguments

# Load and merge all JSON files from the "datasets" directory.
def load_datasets(dataset_dir):
    all_examples = []
    for file in glob.glob(os.path.join(dataset_dir, "*.json")):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_examples.extend(data)
    return all_examples

# Load vocabulary from "vocab" folder and return as a list
def load_vocab(vocab_dir):
    vocab_words = set()
    for file in glob.glob(os.path.join(vocab_dir, "*.json")):
        with open(file, "r", encoding="utf-8") as f:
            words = json.load(f)
            vocab_words.update(words)
    return list(vocab_words)

# Tokenize the data and align labels
def tokenize_and_align_labels(examples, tokenizer):
    texts = [ex[0] for ex in examples]
    tokenized_inputs = tokenizer(
        texts,
        padding=True,
        truncation=True,
        return_offsets_mapping=True,
        is_split_into_words=False
    )
    
    labels_all = []
    for i, example in enumerate(examples):
        entities = example[1]["entities"]
        offset_mapping = tokenized_inputs.offset_mapping[i]
        label_ids = ["O"] * len(offset_mapping)
        
        for start, end, entity_label in entities:
            for idx, (token_start, token_end) in enumerate(offset_mapping):
                if token_start == start:
                    label_ids[idx] = f"B-{entity_label}"
                elif token_start > start and token_end <= end:
                    label_ids[idx] = f"I-{entity_label}"
        labels_all.append(label_ids)
    
    tokenized_inputs["labels"] = labels_all
    tokenized_inputs.pop("offset_mapping")
    return tokenized_inputs

# Create a label mapping
def get_label_mapping(examples):
    label_set = set()
    for ex in examples:
        for _, _, label in ex[1]["entities"]:
            label_set.add(label)
    label_list = sorted(list(label_set))
    label_to_id = {"O": 0}
    idx = 1
    for label in label_list:
        label_to_id[f"B-{label}"] = idx
        idx += 1
        label_to_id[f"I-{label}"] = idx
        idx += 1
    return label_to_id

# Convert labels to IDs
def convert_labels_to_ids(encodings, label_to_id):
    new_labels = []
    for label_seq in encodings["labels"]:
        new_seq = [label_to_id[label] for label in label_seq]
        new_labels.append(new_seq)
    encodings["labels"] = new_labels
    return encodings

# PyTorch dataset class
class NERDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings
    
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        return item
    
    def __len__(self):
        return len(self.encodings["input_ids"])

# Main training pipeline
def main():
    print("CUDA Available:", torch.cuda.is_available())

    dataset_dir = "datasets"  # Folder with JSON dataset files
    vocab_dir = "vocab"  # Folder with JSON vocabulary files
    
    examples = load_datasets(dataset_dir)
    print(f"Loaded {len(examples)} examples.")
    
    # Load tokenizer
    tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
    
    # Add new vocabulary words
    new_vocab = load_vocab(vocab_dir)
    tokenizer.add_tokens(new_vocab)
    print(f"Added {len(new_vocab)} new words to tokenizer.")
    
    encodings = tokenize_and_align_labels(examples, tokenizer)
    label_to_id = get_label_mapping(examples)
    print("Label mapping:", label_to_id)

    with open("label_to_id.json", "w") as file:
        json.dump(label_to_id, file, indent=4) 
    
    encodings = convert_labels_to_ids(encodings, label_to_id)
    dataset = NERDataset(encodings)
    
    # Load pre-trained model and resize embeddings
    model = BertForTokenClassification.from_pretrained("bert-base-uncased", num_labels=len(label_to_id))
    model.resize_token_embeddings(len(tokenizer))
    model = model.to("cuda" if torch.cuda.is_available() else "cpu")
    
    training_args = TrainingArguments(
        output_dir="./bert_ner_model",
        eval_strategy="no",
        learning_rate=5e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_steps=10,
        save_steps=500,
        fp16=torch.cuda.is_available(),
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )
    
    print("Starting training...")
    trainer.train()
    
    # Save model and tokenizer
    model.save_pretrained("./bert_ner_model")
    tokenizer.save_pretrained("./bert_ner_model")
    print("Model training complete and saved.")

if __name__ == "__main__":
    main()
