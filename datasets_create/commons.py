import json
import os
import re

def create_training_example(template, replacements):
    pattern = r'\[([a-zA-Z0-9\-\_]+)\]'
    entities = []
    new_text = ""
    last_end = 0

    for match in re.finditer(pattern, template):
        placeholder = match.group(1)  
        start, end = match.span()

        new_text += template[last_end:start]
        value = str(replacements.get(placeholder, ""))
        new_text += value

        entity_start = len(new_text) - len(value)
        entity_end = len(new_text)
        label = placeholder.replace("-", "_").upper()
        entities.append((entity_start, entity_end, label))
        last_end = end
    new_text += template[last_end:]
    return new_text, {"entities": entities}

templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
filler_values_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fillers'))
datasets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'datasets'))

with open(os.path.join(templates_dir, "noun_con_reg_sub_template.json"), "r", encoding="utf-8") as file:
    noun_geo_template = json.load(file)

with open(os.path.join(filler_values_dir, "noun_con_reg_sub_filler.json"), "r", encoding="utf-8") as file:
    noun_geo_data = json.load(file)

with open(os.path.join(templates_dir, "con_reg_sub_template.json"), "r", encoding="utf-8") as file:
    geo_template = json.load(file)

with open(os.path.join(filler_values_dir, "con_reg_sub_filler.json"), "r", encoding="utf-8") as file:
    geo_data = json.load(file)

with open(os.path.join(templates_dir, "cooking_process_template.json"), "r", encoding="utf-8") as file:
    cooking_process_template = json.load(file)

with open(os.path.join(filler_values_dir, "cooking_process_filler.json"), "r", encoding="utf-8") as file:
    cooking_process_filler = json.load(file)

with open(os.path.join(templates_dir, "ingredient_template.json"), "r", encoding="utf-8") as file:
    ingredient_template = json.load(file)

with open(os.path.join(filler_values_dir, "ingredient_filler.json"), "r", encoding="utf-8") as file:
    ingredient_filler = json.load(file)

with open(os.path.join(templates_dir, "nutrition_template.json"), "r", encoding="utf-8") as f:
    nutrition_template = json.load(f)

with open(os.path.join(filler_values_dir, "nutrition_filler.json"), "r", encoding="utf-8") as f:
    nutrition_filler_data = json.load(f)

with open(os.path.join(templates_dir, "recipe_template.json"), "r", encoding="utf-8") as f:
    recipe_template = json.load(f)

with open(os.path.join(filler_values_dir, "recipe_filler.json"), "r", encoding="utf-8") as f:
    recipe_filler = json.load(f)

with open(os.path.join(templates_dir, "utensil_template.json"), "r", encoding="utf-8") as file:
    utensil_template = json.load(file)

with open(os.path.join(filler_values_dir, "utensil_filler.json"), "r", encoding="utf-8") as file:
    utensil_filler = json.load(file)