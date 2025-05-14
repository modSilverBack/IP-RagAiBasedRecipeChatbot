import spacy

# Function to load the trained model and test it on multiple questions
def test_spacy_ner(model_path, texts):
    # Load the trained model
    nlp = spacy.load(model_path)
    results = []
    
    # Process each text through the model
    for text in texts:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]  # Extract recognized entities
        results.append({"text": text, "entities": entities})
    
    return results

if __name__ == "__main__":
    model_path = "spacy_ner_model"  # Path to your trained model
    test_texts = [
    "How long does it take to cook Sushi?",
    "How do I substitute cream in Sahi Panner?",
    "Which recipes from Nepal use rajma?",
    "Can you explain the difference between baking and frying in cooking chips?", #false
    "What are the top dishes from Iran that require frying?",
    "What is the best way to prepare Kheer, and how does it compare to Payasam in terms of cooking process?",
    "Can you tell me the best way to grill a Salmon Fillet?", # false
    "What pan do I need to prepare French Omelette?", # pan not labeled
    "Is Garlic essential for making Garlic Butter Shrimp?", # garlic labled as recipe
    "Can you explain the difference between Boiling and Steaming in cooking Dumplings?", # wired bihavier
    "What is the best way to prepare Sushi Rolls, and how does it compare to Poke Bowl in terms of Rolling method?", #
    "In India, which traditional dish is made using Slow Cooking with Lamb?",
    "What are the differences between Ratatouille from Provence and Languedoc?",
    "Can you provide a step-by-step guide for cooking Vegan Pasta without using Cheese?",
    "Can you suggest a recipe like Grilled Chicken Salad that stays within 500 kcal but has at least 20g protein and less than 10g fat?"
]
    
    # Run the model on test questions
    results = test_spacy_ner(model_path, test_texts)
    
    # Print the results
    for res in results:
        print(f"Text: {res['text']}")
        print(f"Entities: {res['entities']}")
        print("-" * 40)
