

# RecipeBot: a RAG chatbot using NER and RecipeDb API

## Summary 

RecipeBot is a RAG (Retrieval-Augmented Generation) chatbot, meaning it uses a pretrained LLM, but instead of just passing in the query, it also attaches more information, which is most likely to contain the answer to the query. In RecipeBot, we are doing NER on the query to fill in the fields of the RecipeDb API and attach the API response and web-parsed information from the URL in the API response. We are using RecipeDb as the main source of information, and the chatbot is guided to only answer related questions through RecipeDb.

## Key Features

1. **BERT NER Model** finetuned to recognize the RecipeDb API fields.
  - **Custom Dataset of 6896** examples used for finetuning the BERT model.
  - **Custom Vocab of 2497** words added to the BERT Tokenizer.
3. **RecipeDb API** response is called from the fields filled by the NER model.
4. **Local LLM**, Deepseek R1 1.5B was run locally during the making of this project.
5. **Web Parser**, the Selenium Python library is used to parse the URL in the API responses.
6. **Professional Response Generation**, With the query, the API response, and web information, a prompt is passed to the LLM, which guides it to give professional and relevant answers. 

## RAG Architecture

```
User Query → BERT NER Model → Structured Query Object → RecipeDB API →
Web Parser → RAG Prompt Engineering → DeepSeek R1 LLM → Response
```

## Project Structure

- **Directories**
  1. **manual datasets** have files containing training examples (220 in total) that are manually annotated and a Python script to convert them to a suitable format for BERT. Different files have examples for different types of API fields. eg. recipe_manual.json have examples most focused on the recipe_title API field.
  2. **templates** have different files containing training example templates for particular API fields. For example, con_sub_reg_template.json has templates for continent, sub-region, region, and all combinations of them. A template looks like "Which dish is popular in [continent] cuisine?" where [continent] can be replaced with any continent, and it will become a valid training example. 
  3. **fillers** have different files containing the filler data to populate the templates and make training examples. For example, con_sub_reg_filler.json has a list of all valid continents, sub-regions, and regions for the recipeDb API.
  4. **vocab** has files that have a list of words that are being added to the vocabulary of the BERT Tokenizer for better NER. For example, cooking_process.json has a vocabulary related to cooking processes.
  5. **dataset_create** has the Python script to make training examples using templates and fillers, and put them in the datasets directory(create if it doesn't exist).
- **Files**
  1. **bert_ner.py** concatinates all vocab and adds it to the BERT Tokenizer, concatinates all the training examples and trains the BERT model and saves it in directory bert_ner_model.
  2. **requests.py** gets the API response.
  3. **test_bert.py** has the code for testing the BERT NER model against fixed 20 examples. 
  4. **web_parser.py** gets the information form the URL that are there in the API responses.
  5. **main** the pipeline of the RAG chatbot is implimented here.
  6. **spacy_ner.py** we also tried spacy NER model (it was not up to mark).
  7. **test_spacey_ner.py** testing spacy NER model against same fixed 20 examples.
  8. **testing_gliner_spacy.py** we also tried the pretrained gliner spacy ner model (it was not up to mark).


## Technical Details

### NER fields

```
{
 "O": 0,
 "B-CARBOHYDRATES_MAX": 1,
 "I-CARBOHYDRATES_MAX": 2,
 "B-CARBOHYDRATES_MIN": 3,
 "I-CARBOHYDRATES_MIN": 4,
 "B-CONTINENT": 5,
 "I-CONTINENT": 6,
 "B-COOKING_PROCESS": 7,
 "I-COOKING_PROCESS": 8,
 "B-ENERGY_MAX": 9,
 "I-ENERGY_MAX": 10,
 "B-ENERGY_MIN": 11,
 "I-ENERGY_MIN": 12,
 "B-FAT_MAX": 13,
 "I-FAT_MAX": 14,
 "B-FAT_MIN": 15,
 "I-FAT_MIN": 16,
 "B-INGREDIENT_NOT_USED": 17,
 "I-INGREDIENT_NOT_USED": 18,
 "B-INGREDIENT_USED": 19,
 "I-INGREDIENT_USED": 20,
 "B-PROTEIN_MAX": 21,
 "I-PROTEIN_MAX": 22,
 "B-PROTEIN_MIN": 23,
 "I-PROTEIN_MIN": 24,
 "B-RECIPE_TITLE": 25,
 "I-RECIPE_TITLE": 26,
 "B-REGION": 27,
 "I-REGION": 28,
 "B-SUB_REGION": 29,
 "I-SUB_REGION": 30,
 "B-UTENSIL": 31,
 "I-UTENSIL": 32
}
```


### RAG Prompt 

```
You are a chatbot for answering queries related to different recipes across the world 
which have been mentioned in the recipeDb API. Response of the API is provided along with the list of 
ingredients separately for each api response.
In the API response there is a url you can give back to the user and 
ask them to refer to those links for futher information.
Your answer should be within 100 words. Use a professional tone while interacting with the user.
For any question related to recipes if there is no api response attached in json format, say "That's an
interesting question! But this specific request is a bit outside of what I can currently assist with. 
However, I'm happy to help with something related or guide you in the right direction 
if you'd like!".
For questions not related to recipes, give this response- "That's an 
interesting topic! My main focus is on helping with recipes and cooking-related questions, 
so I might not be the best source for that. But if you have anything food-related in mind, 
I'd love to help!". 
After a question, give users something to do next-"If possible, suggest a topic or ask a 
clarifying question to keep the conversation going.".
Also while answering do the appropriate calculations to find the 
nutrition per serving which is given as per the serving size in the API response.
Below will be the question that is asked to the chatbot you are to function as you have
to answer as if you are answering that question.
```

### Local LLM Integration

The system uses Ollama to run the DeepSeek R1 1.5B model locally, providing:
1. Lower latency responses
2. No external API costs
3. Privacy-preserving operation

**NOTE**: Use of a better LLM will improve the chatbot greatly as the 1.5B model is coming short on many applications, like not understanding the RAG prompt and hallucinating during reasoning. 

### Example Query and Response

**Query**: "Suggest a recipe which involves whisking and has less than 700 cal."

**Response**: 
```
I'd recommend Velouté Sauce (Escoffier's Recipe), a classic French sauce that involves whisking and contains approximately 645.3 calories. This elegant sauce requires butter, flour, white veal stock, button mushrooms, salt, nutmeg, and white pepper. The recipe uses a whisk to combine ingredients and serves 4 quarts.

Nutrition per serving:
Calories: 611.5 kcal
Carbohydrates: 66g
Protein: 14.6g
Fat: 33.8g

For the complete recipe and detailed instructions, check out: http://www.geniuskitchen.com/recipe/veloute-sauce-escoffiers-recipe-469366

Would you like to know more about French sauces or perhaps other low-calorie recipe options?
```

## Future Work

1. The RecipeBot can be deployed to a website to enhance **User Experience** and make it more accessible.
2. **Improve the NER model** The NER model has a lot of scope for improvement.
3. Use of more **powerful LLM** will make RecipeBot more accurate and precise from its current status.  

## Dependencies

- transformers (for BERT NER model)
- requests
- Ollama (for running DeepSeek R1 locally)

## Acknowledgements

All thanks to Ganesh Bagler, sir, at IIIT-D for allowing the team to work on this project's idea. The team is most thankful for the creative freedoms. 
