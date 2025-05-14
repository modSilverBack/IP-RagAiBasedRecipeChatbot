import json
import os
import commons

# Total training examples: 1116

def to_ed(verb):
    irregular = {
        "put": "put",
        "cut": "cut",
        "set": "set",
        "stand": "stood",
        "break": "broke"
    }
    if verb in irregular:
        return irregular[verb]
    if verb.endswith("e"):
        return verb + "d"
    else:
        return verb + "ed"

def to_ing(verb):
    irregular = {
        "put": "putting",
        "cut": "cutting",
        "set": "setting",
        "stand": "standing",
        "break": "breaking"
    }
    if verb in irregular:
        return irregular[verb]
    if verb.endswith("e"):
        return verb[:-1] + "ing"
    else:
        return verb + "ing"

dataset = []

for tmpl in commons.cooking_process_template["base_form"]:
    for cooking_proc in commons.cooking_process_filler:
        text, annotation = commons.create_training_example(tmpl, cooking_proc)
        dataset.append((text, annotation))

cooking_processes = [i["cooking-process"] for i in commons.cooking_process_filler]
for tmpl in commons.cooking_process_template["ing_form"]:
    for cooking_proc in list(map(to_ing, cooking_processes)):
        text, annotation = commons.create_training_example(tmpl, {"cooking-process": cooking_proc})
        dataset.append((text, annotation))


for tmpl in commons.cooking_process_template["ed_form"]:
    for cooking_proc in list(map(to_ed, cooking_processes)):
        text, annotation = commons.create_training_example(tmpl, {"cooking-process": cooking_proc})
        dataset.append((text, annotation))

print("Total training examples:", len(dataset))

with open(os.path.join(commons.datasets_dir, "cooking_process_dataset.json"), "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

