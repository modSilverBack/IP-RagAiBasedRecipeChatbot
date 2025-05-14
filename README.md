# RecipeBot: Named Entity Recognition-powered Recipe Chatbot

## Overview

RecipeBot is an intelligent chatbot system designed to help users discover and understand recipes from around the world. By leveraging a custom-trained BERT Named Entity Recognition (NER) model, a structured recipe database (RecipeDB), and a locally-hosted DeepSeek R1 language model, RecipeBot can process natural language queries and provide relevant recipe information.

The system extracts key entities from user queries (ingredients, cooking processes, nutritional requirements, etc.), retrieves matching recipes from a comprehensive database, and generates helpful responses using a Retrieval-Augmented Generation (RAG) approach.

## Key Features

- **Custom BERT NER Model**: Trained to recognize recipe-specific entities such as ingredients, cooking processes, nutritional values, and regional cuistures
- **Structured Query Generation**: Converts natural language queries into structured API requests
- **Local LLM Integration**: Runs DeepSeek R1 1.5B model locally via Ollama for efficient processing
- **Web Parser**: Extracts detailed ingredient information from recipe URLs
- **Nutrition Calculation**: Performs calculations to determine nutrition per serving
- **Professional Response Generation**: Creates concise, helpful answers with a professional tone

## System Architecture

```
User Query → BERT NER Model → Structured Query Object → RecipeDB API →
Web Parser (for ingredient details) → RAG Prompt Engineering → DeepSeek R1 LLM → Response
```

## Project Structure

```
project/
├── _pycache_/                   # Python cache files
├── bert_ner_model/              # BERT NER model files
├── datasets/                    # Training datasets
│   ├── con_reg_sub_dataset.json
│   ├── cooking_process_dataset.json
│   ├── diverse_manual_dataset.json
│   ├── ingredient_dataset.json
│   ├── noun_con_reg_sub_dataset.json
│   ├── nutrition_dataset.json
│   ├── nutrition_manual_dataset.json
│   ├── recipe_dataset.json
│   ├── recipe_manual_dataset.json
│   ├── utensil_dataset.json
│   └── utensil_manual_dataset.json
├── datasets_create/             # Scripts to create datasets
├── fillers/                     # JSON fillers for data processing
├── manual_datasets/             # Manually created datasets
├── templates/                   # JSON templates
├── vocab/                       # Vocabulary files for NER model
│   ├── con_reg_sub_vocab.json
│   ├── cooking_process_vocab.json
│   ├── ingredient_vocab.json
│   ├── noun_con_sub_vocab.json
│   ├── recipe_vocab.json
│   └── utensil_vocab.json
├── bert_ner.py                  # BERT NER model implementation
├── label_to_id.json             # Label to ID mapping
├── main.py                      # Main application entry point
├── README.md                    # This file
├── request.py                   # API request handler
├── spacy_ner.py                 # SpaCy NER implementation
├── test_bert_ner.py             # Testing script for BERT NER
├── test_spacy_ner.py            # Testing script for SpaCy NER
├── testing_aliner_spacy.py      # Testing script for SpaCy aliner
└── web_parser.py                # Parser for extracting data from recipe websites
```

## Technical Details

### NER Model Training

The system uses a custom BERT-based Named Entity Recognition model trained on domain-specific datasets for:
- Ingredients
- Cooking processes
- Continents, regions, and sub-regions
- Recipe titles
- Utensils
- Nutritional requirements (calories, carbohydrates, protein, fat)

The model can identify multiple entity types, including:
- B-CONTINENT
- B-REGION
- B-SUB_REGION
- B-RECIPE_TITLE
- B-INGREDIENT_USED
- B-INGREDIENT_NOT_USED
- B-COOKING_PROCESS
- B-UTENSIL
- B-ENERGY_MIN/MAX
- B-CARBOHYDRATES_MIN/MAX
- B-FAT_MIN/MAX
- B-PROTEIN_MIN/MAX

### Query Processing Pipeline

1. **Entity Extraction**: The NER model extracts relevant entities from the user query
2. **Query Object Construction**: Builds a structured query object with extracted entities
3. **API Request**: Sends the query object to the RecipeDB API
4. **Response Processing**: Formats the API response for the RAG prompt
5. **LLM Generation**: Uses the DeepSeek R1 model to generate the final response

### RAG Implementation

The RAG prompt combines:
- System instructions for the chatbot behavior
- The original user query
- The structured API response with recipe data
- Ingredient details (from web parsing if needed)

This combined context allows the LLM to generate responses that incorporate both the retrieved information and general language capabilities.

### Local LLM Integration

The system uses Ollama to run the DeepSeek R1 1.5B model locally, providing:
- Lower latency responses
- No external API costs
- Privacy-preserving operation

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/recipebot.git
cd recipebot

# Install dependencies
pip install -r requirements.txt

# Make sure Ollama is installed and running
# https://ollama.ai/download

# Pull the DeepSeek model
ollama pull deepseek-r1:1.5b

# Set up environment variables (if needed)
cp .env.example .env
# Edit .env file with your configuration
```

## Usage

### Running the Bot

```python
from main import exec_rag

# Ask a recipe-related question
query = "Suggest a recipe which involves whisking and have less than 700 cal."
response, api_data = exec_rag(query)
print(response)
```

### Example Query and Response

**Query**: "Suggest a recipe which involves whisking and have less than 700 cal."

**Response**: 
```
I'd recommend Veloute Sauce (Escoffier's Recipe), a classic French sauce that involves whisking and contains approximately 645.3 calories. This elegant sauce requires butter, flour, white veal stock, button mushrooms, salt, nutmeg, and white pepper. The recipe uses a whisk to combine ingredients and serves 4 quarts.

Nutrition per serving:
Calories: 611.5 kcal
Carbohydrates: 66g
Protein: 14.6g
Fat: 33.8g

For the complete recipe and detailed instructions, check out: http://www.geniuskitchen.com/recipe/veloute-sauce-escoffiers-recipe-469366

Would you like to know more about French sauces or perhaps other low-calorie recipe options?
```

## Future Improvements

- **Enhanced NER Model**: 
  - Collect more diverse training data for better entity recognition
  - Implement active learning to improve entity identification in edge cases
  - Explore transformer models beyond BERT for potential accuracy improvements
  - Add support for more languages to handle international recipe queries

- **Advanced Query Processing**:
  - Implement query expansion techniques to handle synonyms and related terms
  - Add fuzzy matching for ingredient detection
  - Incorporate semantic understanding of cooking techniques and substitutions

- **Improved Database Integration**:
  - Expand the recipe database with more diverse cuisines and regional variations
  - Add support for dietary restrictions (vegan, gluten-free, keto, etc.)
  - Include seasonal recipe recommendations based on available ingredients

- **User Experience**:
  - Develop a responsive web interface with recipe cards and images
  - Create a mobile application for on-the-go recipe assistance
  - Implement voice input for hands-free cooking assistance
  - Add personalization features to remember user preferences

- **Enhanced Response Generation**:
  - Fine-tune the RAG prompt for more natural conversational flow
  - Add support for step-by-step cooking instructions
  - Implement meal planning capabilities for weekly recipe suggestions
  - Include smart substitution recommendations for unavailable ingredients

- **Technical Improvements**:
  - Optimize the web parser for faster ingredient extraction
  - Implement caching for frequently requested recipes
  - Add support for larger language models as hardware permits
  - Create a distributed architecture for better scalability

- **Additional Features**:
  - Implement image recognition for ingredient identification
  - Add support for recipe scaling (adjust servings)
  - Include shopping list generation from selected recipes
  - Develop a recommendation system based on user history

## Dependencies

- transformers (for BERT NER model)
- requests
- spacy (for alternative NER implementation)
- Ollama (for running DeepSeek R1 locally)

## License

[MIT License](LICENSE)

## Acknowledgements

- Thanks to the DeepSeek team for their excellent LLM
- BERT model architecture from Google Research
- Recipe data sources used in building RecipeDB