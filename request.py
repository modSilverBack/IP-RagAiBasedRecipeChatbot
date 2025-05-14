import requests

url = "https://cosylab.iiitd.edu.in/recipe-search/recipesAdvanced?page=1&pageSize=2"

headers = {'x-API-key': 'cosylab'}

query_obj = {
    "continent": "Asian",
    "region": "",
    "subRegion": "",
    "recipeTitle": "",
    "ingredientUsed": "",
    "ingredientNotUsed": "",
    "cookingProcess": "",
    "utensil": "",
    "energyMin": 0,
    "energyMax": 0,
    "carbohydratesMin": 0,
    "carbohydratesMax": 0,
    "fatMin": 0,
    "fatMax": 0,
    "proteinMin": 0,
    "proteinMax": 0
}


def query(query_obj):
    global headers
    response = requests.post(url, json=query_obj, headers=headers)
    print(response.status_code)
    print(response.text)
    data = (response.json())

    if data["success"] == "true":
        return data
    else:
        return "no such recipe found!"

# not working as this api is no longer supported 
if __name__ == "__main__":
    print(query(query_obj=query_obj))
    
# data = { 
#     "success": "true",
#     "message": "Recipes fetched successfully.",
#     "payload": {
#         "data": [
#             {
#                 "Recipe_id": "116780",
#                 "Calories": "645.3",
#                 "total_time": "125",
#                 "Recipe_title": "Veloute Sauce (Escoffier's Recipe)",
#                 "url": "http://www.geniuskitchen.com/recipe/veloute-sauce-escoffiers-recipe-469366",
#                 "Region": "French",
#                 "Utensils": "whisk||saucepan",
#                 "Processes": "heat||melt||whisk||cook"
#             },
#             {
#                 "Recipe_id": "84021",
#                 "Calories": "635.5",
#                 "total_time": "30",
#                 "Recipe_title": "Ice Cream with Mexican Chocolate",
#                 "url": "http://www.geniuskitchen.com/recipe/ice-cream-with-mexican-chocolate-74328",
#                 "Region": "Mexican",
#                 "Utensils": "bowl||whisk||saucepan",
#                 "Processes": "put||whisk||whisk||melt"
#             }
#         ]
#     }
# }