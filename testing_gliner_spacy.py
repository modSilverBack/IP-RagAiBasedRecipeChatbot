import spacy
from gliner_spacy.pipeline import GlinerSpacy

nlp = spacy.load("en_core_web_sm")
labels = [
    "continent", "region", "subRegion", "recipeTitle", "ingredientUsed",
    "ingredientNotUsed", "cookingProcess", "utensil", "energyMin", "energyMax",
    "carbohydratesMin", "carbohydratesMax", "fatMin", "fatMax", "proteinMin", "proteinMax"]

nlp.add_pipe("gliner_spacy", config={"labels": labels})

doc = nlp("What dishes are similar to rajma and have at lest 12 grams of protein per serving in india?")

for ent in doc.ents:
    print(ent.text, ent.label_)

# NOT UP TO MARK