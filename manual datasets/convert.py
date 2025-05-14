import json
import os


# Total training examples: 78

file_path = os.path.join(os.path.dirname(__file__), "recipe_manual.json")
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

converted_data = []

for entry in data:
    text = entry["text"]
    entities = []

    for entity in entry["entities"]:
        entity_text = entity["entity"]
        label = entity["label"].replace("-", "_").upper()

        start_idx = text.find(entity_text)
        if start_idx != -1:
            end_idx = start_idx + len(entity_text)
            entities.append([start_idx, end_idx, label])

    converted_data.append([text, {"entities": entities}])

datasets_dir = os.path.join(os.path.dirname(__file__), "..", 'datasets')

with open(os.path.join(datasets_dir, "recipe_manual_dataset.json"), "w", encoding="utf-8") as file:
    json.dump(converted_data, file, indent=4, ensure_ascii=False)

print("Total training examples:", len(converted_data))


# Total training examples: 58

file_path = os.path.join(os.path.dirname(__file__), "utensil_manual.json")
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

converted_data = []

for entry in data:
    text = entry["text"]
    entities = []

    for entity in entry["entities"]:
        entity_text = entity["entity"]
        label = entity["label"].replace("-", "_").upper()

        start_idx = text.find(entity_text)
        if start_idx != -1:
            end_idx = start_idx + len(entity_text)
            entities.append([start_idx, end_idx, label])

    converted_data.append([text, {"entities": entities}])

datasets_dir = os.path.join(os.path.dirname(__file__), "..", 'datasets')

with open(os.path.join(datasets_dir, "utensil_manual_dataset.json"), "w", encoding="utf-8") as file:
    json.dump(converted_data, file, indent=4, ensure_ascii=False)

print("Total training examples:", len(converted_data))

# Total training examples: 17

file_path = os.path.join(os.path.dirname(__file__), "nutrition_manual.json")
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

converted_data = []

for entry in data:
    text = entry["text"]
    entities = []

    for entity in entry["entities"]:
        entity_text = entity["entity"]
        label = entity["label"].replace("-", "_").upper()

        start_idx = text.find(entity_text)
        if start_idx != -1:
            end_idx = start_idx + len(entity_text)
            entities.append([start_idx, end_idx, label])

    converted_data.append([text, {"entities": entities}])

datasets_dir = os.path.join(os.path.dirname(__file__), "..", 'datasets')

with open(os.path.join(datasets_dir, "nutrition_manual_dataset.json"), "w", encoding="utf-8") as file:
    json.dump(converted_data, file, indent=4, ensure_ascii=False)

print("Total training examples:", len(converted_data))

# Total training examples: 67

file_path = os.path.join(os.path.dirname(__file__), "diverse_manual.json")
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

converted_data = []

for entry in data:
    text = entry["text"]
    entities = []

    for entity in entry["entities"]:
        entity_text = entity["entity"]
        label = entity["label"].replace("-", "_").upper()

        start_idx = text.find(entity_text)
        if start_idx != -1:
            end_idx = start_idx + len(entity_text)
            entities.append([start_idx, end_idx, label])

    converted_data.append([text, {"entities": entities}])

datasets_dir = os.path.join(os.path.dirname(__file__), "..", 'datasets')

with open(os.path.join(datasets_dir, "diverse_manual_dataset.json"), "w", encoding="utf-8") as file:
    json.dump(converted_data, file, indent=4, ensure_ascii=False)

print("Total training examples:", len(converted_data))