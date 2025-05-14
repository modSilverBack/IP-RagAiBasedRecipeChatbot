import json
import os
import commons

# Total training examples: 1554

dataset = []

for template in commons.recipe_template["recipe_title"]:
    for dish in commons.recipe_filler:
        text, annotation = commons.create_training_example(template, dish)
        dataset.append((text, annotation))


for template in commons.recipe_template["recipe_title"]:
    for dish in list(zip(commons.recipe_filler[:len(commons.recipe_filler)-1], commons.recipe_filler[1:]))[:10]:
        repl = {"recipe_title0": dish[0]["recipe_title"], "recipe_title1": dish[0]["recipe_title"]}
        text, annotation = commons.create_training_example(template, repl)
        dataset.append((text, annotation))

for template in commons.recipe_template["recipe_title"]:
    for dish in list(zip(commons.recipe_filler[:len(commons.recipe_filler)-2], commons.recipe_filler[1:len(commons.recipe_filler)-1], commons.recipe_filler[2:]))[:10]:
        repl = {"recipe_title0": dish[0]["recipe_title"], "recipe_title1": dish[0]["recipe_title"], "recipe_title2": dish[2]["recipe_title"]}
        text, annotation = commons.create_training_example(template, repl)
        dataset.append((text, annotation))

print("Total training examples:", len(dataset))

with open(os.path.join(commons.datasets_dir, "recipe_dataset.json"), "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

