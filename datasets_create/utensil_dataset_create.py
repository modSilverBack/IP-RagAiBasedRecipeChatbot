import json
import os
import commons

# Total training examples: 1170

dataset = []

for template in commons.utensil_template:
    for utensil in commons.utensil_filler:
        text, annotation = commons.create_training_example(template, utensil)
        dataset.append((text, annotation))

with open(os.path.join(commons.datasets_dir, "utensil_dataset.json"), "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print("Total training examples:", len(dataset))

