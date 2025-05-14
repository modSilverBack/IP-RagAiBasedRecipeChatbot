import json
import os
import random
import commons

# Total training examples: 1010

dataset = []

for tmpl in commons.ingredient_template["ingredient_used"]:
    for ing in commons.ingredient_filler:
        text, annotation = commons.create_training_example(tmpl, {"ingredient-used": ing})
        dataset.append((text, annotation))

for tmpl in commons.ingredient_template["ingredient_not_used"]:
    for ing in commons.ingredient_filler:
        text, annotation = commons.create_training_example(tmpl, {"ingredient-not-used": ing})
        dataset.append((text, annotation))

ing_list = list(commons.ingredient_filler)
random.shuffle(ing_list)
for tmpl in commons.ingredient_template["combined"]:
    for ing_used in ing_list[:10]:
        for ing_not in ing_list[10:20]:
            text, annotation = commons.create_training_example(tmpl, replacements = {"ingredient-used": ing_used, "ingredient-not-used": ing_not})
            dataset.append((text, annotation))

print("Total training examples:", len(dataset))

with open(os.path.join(commons.datasets_dir, "ingredient_dataset.json"), "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

