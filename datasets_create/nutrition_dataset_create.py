import json
import os
import commons

# Total training examples: 456

dataset = []

simple_keys = [
    "protein_min", "protein_max", "energy_min", "energy_max",
    "carbohydrates_min", "carbohydrates_max", "fat_min", "fat_max"
]

for key in simple_keys:
    for template in commons.nutrition_template[key]:
        for val in commons.nutrition_filler_data.get(key, []):
            text, annotation = commons.create_training_example(template, { key: str(val) })
            dataset.append((text, annotation))

combined_keys = [
    "protein_min_protein_max_combined", "energy_min_energy_max_combined",
    "carbohydrates_min_carbohydrates_max_combined", "fat_min_fat_max_combined"
]

for key in combined_keys:
    tmp_split = key.split("_")
    first_key = tmp_split[0] + "_" +tmp_split[1]
    second_key = tmp_split[2] + "_" + tmp_split[3]
    for template in commons.nutrition_template[key]:
        for nutr0, nutr1 in zip(commons.nutrition_filler_data[first_key], commons.nutrition_filler_data[second_key]):
            text, annotation = commons.create_training_example(template, {first_key: str(nutr0), second_key: str(nutr1)})
            dataset.append((text, annotation))
    
f_mins = commons.nutrition_filler_data["fat_min"]
f_maxs = commons.nutrition_filler_data["fat_max"]
c_mins = commons.nutrition_filler_data["carbohydrates_min"]
c_maxs = commons.nutrition_filler_data["carbohydrates_max"]
p_mins = commons.nutrition_filler_data["protein_min"]
p_maxs = commons.nutrition_filler_data["protein_max"]
e_mins = commons.nutrition_filler_data["energy_min"]
e_maxs = commons.nutrition_filler_data["energy_max"]

all_nutr = zip(f_mins, f_maxs, c_mins, c_maxs, e_mins, e_maxs, p_mins, p_maxs)
all_nutr_replacement = [
    {"fat_min": f_min, "fat_max": f_max, "carbohydrates_min": c_min, "carbohydrates_max": c_max,
    "energy_min": e_min, "energy_max": e_max, "protein_min": p_min, "protein_max": p_max}
    for f_min, f_max, c_min, c_max, e_min, e_max, p_min, p_max in all_nutr
]

for template in commons.nutrition_template["all_nutrition_combined"]:
    for repl in all_nutr_replacement:
        text, annotation = commons.create_training_example(template, repl)
        dataset.append((text, annotation))

print("Total training examples:", len(dataset))

with open(os.path.join(commons.datasets_dir, "nutrition_dataset.json"), "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

