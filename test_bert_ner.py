from transformers import BertForTokenClassification, BertTokenizerFast, pipeline

def label_index_to_name(label_index):
    label_mapping = {
        "LABEL_0": 'O', "LABEL_1": 'B-CARBOHYDRATES_MAX', "LABEL_2": 'I-CARBOHYDRATES_MAX', "LABEL_3": 'B-CARBOHYDRATES_MIN',
        "LABEL_4": 'I-CARBOHYDRATES_MIN', "LABEL_5": 'B-CONTINENT', "LABEL_6": 'I-CONTINENT', "LABEL_7": 'B-COOKING_PROCESS',
        "LABEL_8": 'I-COOKING_PROCESS', "LABEL_9": 'B-ENERGY_MAX', "LABEL_10": 'I-ENERGY_MAX', "LABEL_11": 'B-ENERGY_MIN',
        "LABEL_12": 'I-ENERGY_MIN', "LABEL_13": 'B-FAT_MAX', "LABEL_14": 'I-FAT_MAX', "LABEL_15": 'B-FAT_MIN', "LABEL_16": 'I-FAT_MIN',
        "LABEL_17": 'B-INGREDIENT_NOT_USED', "LABEL_18": 'I-INGREDIENT_NOT_USED', "LABEL_19": 'B-INGREDIENT_USED',
        "LABEL_20": 'I-INGREDIENT_USED', "LABEL_21": 'B-PROTEIN_MAX', "LABEL_22": 'I-PROTEIN_MAX', "LABEL_23": 'B-PROTEIN_MIN',
        "LABEL_24": 'I-PROTEIN_MIN', "LABEL_25": 'B-RECIPE_TITLE', "LABEL_26": 'I-RECIPE_TITLE', "LABEL_27": 'B-REGION',
        "LABEL_28": 'I-REGION', "LABEL_29": 'B-SUB_REGION', "LABEL_30": 'I-SUB_REGION', "LABEL_31": 'B-UTENSIL', "LABEL_32": 'I-UTENSIL'
    }
    return label_mapping[label_index]

# Load Trained Model
model_path = "bert_ner_model"
model = BertForTokenClassification.from_pretrained(model_path)
tokenizer = BertTokenizerFast.from_pretrained(model_path)

# Create NER Pipeline
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Test on New Questions
test_questions = [
    "Suggest a recipe which requires whish and involves whisking and have less than 700 cal."
    # "How long does it take to cook Sushi?",
    # "How do I substitute cream in Sahi Paneer?",
    # "Which recipes from Nepal use rajma?",
    # "Can you explain the difference between baking and frying in cooking chips?",
    # "What are the top dishes from Iran that require frying?",
    # "What is the best way to prepare Kheer, and how does it compare to Payasam in terms of cooking process?",
    # "Can you tell me the best way to grill a Salmon Fillet?",
    # "What pan do I need to prepare French Omelette?",
    # "Is Garlic essential for making Garlic Butter Shrimp?",
    # "Can you explain the difference between Boiling and Steaming in cooking Dumplings?", 
    # "What is the best way to prepare Sushi Rolls, and how does it compare to Poke Bowl in terms of Rolling method?", 
    # "In India, which traditional dish is made using Slow Cooking with Lamb?",
    # "What are the differences between Ratatouille from Provence and Languedoc?",
    # "Can you provide a step-by-step guide for cooking Vegan Pasta without using Cheese?",
    # "Can you suggest a recipe like Grilled Chicken Salad that stays within 500 kcal but has at least 20g protein and less than 10g fat?"
]

# Run inference
for question in test_questions:
    print(f"Question: {question}")
    entities = ner_pipeline(question)
    print("Entities: (Label, Word, Score)")
    ents = [(label_index_to_name(i["entity_group"]), i["word"], i["score"]) for i in entities]
    for i in ents:
        print(i)
    print("-" * 50)
