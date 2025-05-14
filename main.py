import requests
import test_bert_ner
import request

def chat_with_ollama(prompt, model="deepseek-r1:1.5b"):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result["response"]
    else:
        return f"Error {response.status_code}: {response.text}"


rag_prompt = """
You are a chatbot for answering queries related to different recipes across the world 
which have been mentioned in the recipeDb API. you will be provided with the list of 
ingredients separately. 
In the API response you can give the url back to the user and 
ask them to refer to those links for futher information. Your answer should be within 
100 words. Use a professional tone while interacting with the user. For any question 
related to recipes if there is no api respose attached in json formate, say "That's an
interesting question! 
But this specific request is a bit outside of what I can currently assist with. 
However, I'm happy to help with something related or guide you in the right direction 
if you'd like!". For questions not related to recipes, give this respose- "That’s an 
interesting topic! My main focus is on helping with recipes and cooking-related questions, 
so I might not be the best source for that. But if you have anything food-related in mind, 
I'd love to help!". 
After a question, give users something to do next-"If possible, suggest a topic or ask a 
clarifying question to keep the conversation going."
Also while answering do the appropriate calculations to find the 
nutrition per serving which is given as per the serving size in the API response.
below will be the question that is asked to the chatbot you are to function as you have
to answer as if you are answering that question.
make the api respose that is also attached below is not form the urls in the repose they
are link to the orginal website from where the database is made.
"""

def extract_entities_as_dict(text):
    """
    Extracts entities from the text and organizes them as a dictionary.
    """
    entities = test_bert_ner.ner_pipeline(text)
    entities_dict = {}

    for entity in entities:
        label = test_bert_ner.label_index_to_name(entity["entity_group"])
        word = entity["word"]
        
        # Handle subword tokens like "##ing"
        if word.startswith("##"):
            word = word[2:]
        
        # Append or create new entry
        if label in entities_dict:
            entities_dict[label].append(word)
        else:
            entities_dict[label] = [word]
    
    return entities_dict

def exec_rag(query: str) -> tuple[str, str]:
    entities = extract_entities_as_dict(query)

    # Construct the query object
    query_obj = {
        "continent": " ".join(entities.get("B-CONTINENT", [])),
        "region": " ".join(entities.get("B-REGION", [])),
        "subRegion": " ".join(entities.get("B-SUB_REGION", [])),
        "recipeTitle": " ".join(entities.get("B-RECIPE_TITLE", [])),
        "ingredientUsed": " ".join(entities.get("B-INGREDIENT_USED", [])),
        "ingredientNotUsed": " ".join(entities.get("B-INGREDIENT_NOT_USED", [])),
        "cookingProcess": " ".join(entities.get("B-COOKING_PROCESS", [])),
        "utensil": " ".join(entities.get("B-UTENSIL", [])),
        "energyMin": int(entities.get("B-ENERGY_MIN", ["0"])[0]),
        "energyMax": int(entities.get("B-ENERGY_MAX", ["0"])[0]),
        "carbohydratesMin": int(entities.get("B-CARBOHYDRATES_MIN", ["0"])[0]),
        "carbohydratesMax": int(entities.get("B-CARBOHYDRATES_MAX", ["0"])[0]),
        "fatMin": int(entities.get("B-FAT_MIN", ["0"])[0]),
        "fatMax": int(entities.get("B-FAT_MAX", ["0"])[0]),
        "proteinMin": int(entities.get("B-PROTEIN_MIN", ["0"])[0]),
        "proteinMax": int(entities.get("B-PROTEIN_MAX", ["0"])[0])
    }

    # Query the API
    api_response = request.query(query_obj)

    # Prepare API response for chatbot
    if api_response == "no such recipe found!":
        api_response_str = ""
    else:
        api_response_str = str(api_response)

    # Prepare RAG prompt
    rag_prompt = f"""
    propt on what to do: {rag_prompt}
    the question asked by the user: {query}
    the api response: {api_response_str}
    """

    # Get response from chatbot
    chatbot_response = chat_with_ollama(rag_prompt)

    return chatbot_response, api_response_str


def do_example():
  global rag_prompt

  user_input = "Suggest a recipe which involves whisking and have less than 700 cal."

  API_respose = """" 
  {
    "success": "true",
    "message": "Recipes fetched successfully.",
    "payload": {
      "data": [
        {
          "Recipe_id": "116780",
          "Calories": "645.3",
          "cook_time": "0",
          "prep_time": "0",
          "servings": "4 quarts",
          "Recipe_title": "Veloute Sauce (Escoffier's Recipe)",
          "total_time": "125",
          "url": "http://www.geniuskitchen.com/recipe/veloute-sauce-escoffiers-recipe-469366",
          "Region": "French",
          "Sub_region": "French",
          "Continent": "European",
          "Source": "Geniuskitchen",
          "img_url": "https://geniuskitchen.sndimg.com/gk/img/gk-shareGraphic.png",
          "Carbohydrate, by difference (g)": "264.0176",
          "Energy (kcal)": "2446.1204",
          "Protein (g)": "58.4321",
          "Total lipid (fat) (g)": "135.3974",
          "Utensils": "whisk||saucepan",
          "Processes": "heat||melt||whisk||cook||combine||whisk||add||simmer||add||strain||add||cool||cool",
          "vegan": "0.0",
          "pescetarian": "0.0",
          "ovo_vegetarian": "0.0",
          "lacto_vegetarian": "0.0",
          "ovo_lacto_vegetarian": "0.0",
          "id": "640572e3a13d0d2d358a5c23"
        }
      ]
  }
  """

  ingre = """"
  Ingredients:
  8 ounces butter
  9 ounces flour
  5 quarts white veal stock, room-temperature (use Basic White Stock)
  1/4 lb button mushroom, sliced
  1 ounce salt
  1 pinch ground nutmeg
  1 pinch white pepper
  """
  response = chat_with_ollama("propt on what to do: "+rag_prompt +\
                              "the question asked by the user: "+user_input +\
                              "the api respose: "+ API_respose +\
                              "the listo ofingredients of the recipe in the api response: " +  ingre)
  print("🧠 Model says:\n", response)
    

