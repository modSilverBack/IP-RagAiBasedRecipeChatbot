import json
import os
import random
import commons

# Total training examples: 755

dataset = []

unique_continents = {item["continent"] for item in commons.noun_geo_data}
for tmpl in commons.noun_geo_template["continent"]:
    for cont in unique_continents:
        text, ann = commons.create_training_example(tmpl, {"continent": cont})
        dataset.append((text, ann))

unique_regions = {item["region"] for item in commons.noun_geo_data}
for tmpl in commons.noun_geo_template["region"]:
    for reg in unique_regions:
        text, ann = commons.create_training_example(tmpl, {"region": reg})
        dataset.append((text, ann))

unique_sub_regions = {item["sub-region"] for item in commons.noun_geo_data}
for tmpl in commons.noun_geo_template["sub_region"]:
    for sub in unique_sub_regions:
        text, ann = commons.create_training_example(tmpl, {"sub-region": sub})
        dataset.append((text, ann))

continent_region_pairs = list({(item["continent"], item["region"]) for item in commons.noun_geo_data})
random.shuffle(continent_region_pairs)
for tmpl in commons.noun_geo_template["continent_region"]:
    for cont, reg in continent_region_pairs[:10]:
        text, ann = commons.create_training_example(tmpl, {"continent": cont, "region": reg})
        dataset.append((text, ann))

continent_sub_pairs = list({(item["continent"], item["sub-region"]) for item in commons.noun_geo_data})
random.shuffle(continent_sub_pairs)
for tmpl in commons.noun_geo_template["continent_sub_region"]:
    for cont, sub in continent_sub_pairs[:10]:
        text, ann = commons.create_training_example(tmpl, {"continent": cont, "sub-region": sub})
        dataset.append((text, ann))

region_sub_pairs = list({(item["region"], item["sub-region"]) for item in commons.noun_geo_data})
random.shuffle(region_sub_pairs)
for tmpl in commons.noun_geo_template["region_sub_region"]:
    for reg, sub in region_sub_pairs[:10]:
        text, ann = commons.create_training_example(tmpl, {"region": reg, "sub-region": sub})
        dataset.append((text, ann))

all_three = list(commons.noun_geo_data)
random.shuffle(all_three)
for tmpl in commons.noun_geo_template["all_three"]:
    for item in all_three[:10]:
        text, ann = commons.create_training_example(
            tmpl, item
        )
        dataset.append((text, ann))

print("Total training examples:", len(dataset))

with open(os.path.join(commons.datasets_dir, "noun_con_reg_sub_dataset.json"), "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)
