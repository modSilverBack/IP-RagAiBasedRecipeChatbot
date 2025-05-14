import spacy
import json
import glob
import random
from spacy.training.example import Example

# Load dataset from JSON files
def load_datasets(dataset_dir):
    all_examples = []
    for file in glob.glob(f"{dataset_dir}/*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Data should be a list of examples.
            if isinstance(data, list):
                all_examples.extend(data)
            else:
                print(f"Warning: Skipping file {file} due to incorrect format (not a list).")
    return all_examples

# Print sample dataset entries for debugging
def print_sample_data(examples, num_samples=5):
    print("\nSample Training Data Entries:")
    for i, entry in enumerate(examples[:num_samples]):
        # Handle both dictionary and list format entries.
        if isinstance(entry, dict):
            text = entry.get("text", "")
            entities = entry.get("entities", [])
        elif isinstance(entry, list) and len(entry) >= 2:
            text = entry[0]
            # If the second element is a dict with key "entities"
            if isinstance(entry[1], dict) and "entities" in entry[1]:
                entities = entry[1]["entities"]
            else:
                entities = []
        else:
            text = ""
            entities = []
        print(f"Example {i+1}:")
        print(f"Text: {text}")
        print(f"Entities: {entities}")
        print("-" * 40)

def create_spacy_training_data(examples, nlp):
    training_data = []
    for entry in examples:
        # Expect entry to be a list: [text, {"entities": [...] }]
        if isinstance(entry, list) and len(entry) >= 2:
            text = entry[0]
            raw_annotations = entry[1].get("entities", [])
        else:
            print(f"Skipping invalid entry: {entry}")
            continue

        doc = nlp.make_doc(text)
        entities = []  # This will hold the aligned entity annotations
        
        for entity in raw_annotations:
            # Each entity should be a list: [start, end, label]
            if not (isinstance(entity, list) and len(entity) == 3):
                print(f"Skipping malformed entity in '{text}': {entity}")
                continue
            start, end, label = entity
            # Try to align using "expand" mode to be more forgiving
            span = doc.char_span(start, end, label=label, alignment_mode="expand")
            if span is not None:
                # Append the actual (start_char, end_char, label) from the span.
                entities.append((span.start_char, span.end_char, span.label_))
            else:
                print(f"Skipping misaligned entity in '{text}': {entity}")

        annots = {"entities": entities}
        try:
            example = Example.from_dict(doc, annots)
            training_data.append(example)
        except ValueError as e:
            print(f"Skipping misaligned example in '{text}' due to {e}")
    
    return training_data




# Train SpaCy NER model
def train_spacy_ner(dataset_dir, model_path, n_iter=20):
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner", last=True)
    
    examples = load_datasets(dataset_dir)
    print(f"Loaded {len(examples)} examples.")
    
    # Print sample data to verify parsing
    print_sample_data(examples, num_samples=5)
    
    # Collect all entity labels and add them to the NER pipeline.
    entity_labels = set()
    for entry in examples:
        if isinstance(entry, dict):
            annotations = entry.get("entities", [])
        elif isinstance(entry, list) and len(entry) >= 2:
            if isinstance(entry[1], dict):
                annotations = entry[1].get("entities", [])
            else:
                continue
        else:
            continue
        
        for entity in annotations:
            if isinstance(entity, list) and len(entity) == 3:
                label = entity[2]
                entity_labels.add(label)
                ner.add_label(label)
    
    print("\nEntity Labels in Model:")
    for label in sorted(entity_labels):
        print(f" - {label}")
    
    training_data = create_spacy_training_data(examples, nlp)
    
    optimizer = nlp.begin_training()
    for i in range(n_iter):
        random.shuffle(training_data)
        losses = {}
        for example in training_data:
            nlp.update([example], drop=0.5, losses=losses)
        print(f"Iteration {i+1}, Loss: {losses}")
    
    nlp.to_disk(model_path)
    print(f"Model saved to {model_path}")

# Load and test the trained model
def test_spacy_ner(model_path, texts):
    nlp = spacy.load(model_path)
    results = []
    for text in texts:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        results.append({"text": text, "entities": entities})
    return results

if __name__ == "__main__":
    dataset_dir = "datasets"         # Folder with your JSON files
    model_path = "spacy_ner_model"     # Folder where model will be saved
    
    # Train and save the model
    train_spacy_ner(dataset_dir, model_path)
    
    # Test the trained model on multiple sentences
    test_texts = [
        "I want to cook Paneer Butter Masala with a pressure cooker.",
        "Can you suggest a recipe from Italian cuisine?",
        "What are some dishes that use turmeric?",
        "Find me a dessert recipe without eggs."
    ]
    
    results = test_spacy_ner(model_path, test_texts)
    
    print("\nTest Results:")
    for res in results:
        print(f"Text: {res['text']}")
        print(f"Entities: {res['entities']}")
        print("-" * 40)
