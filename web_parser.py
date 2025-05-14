from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse


def get_ingredients_from_url(url: str) -> list[str]:
    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")

    # Set up driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        domain = urlparse(url).netloc

        ingredients = []

        if "allrecipes.com" in domain:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mm-recipes-structured-ingredients__list"))
            )
            ingredient_items = driver.find_elements(By.CLASS_NAME, "mm-recipes-structured-ingredients__list-item")

            for item in ingredient_items:
                try:
                    quantity = item.find_element(By.CSS_SELECTOR, "[data-ingredient-quantity='true']").text
                except:
                    quantity = ""

                try:
                    unit = item.find_element(By.CSS_SELECTOR, "[data-ingredient-unit='true']").text
                except:
                    unit = ""

                try:
                    name = item.find_element(By.CSS_SELECTOR, "[data-ingredient-name='true']").text
                except:
                    name = ""

                ingredient = f"{quantity} {unit} {name}".strip()
                ingredients.append(ingredient)

        elif "geniuskitchen.com" in domain:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ingredient-list"))
            )
            ingredient_items = driver.find_elements(By.CSS_SELECTOR, "ul.ingredient-list > li")

            for item in ingredient_items:
                try:
                    quantity = item.find_element(By.CLASS_NAME, "ingredient-quantity").text
                except:
                    quantity = ""

                try:
                    name = item.find_element(By.CLASS_NAME, "ingredient-text").text
                except:
                    name = ""

                ingredient = f"{quantity} {name}".strip()
                ingredients.append(ingredient)

        else:
            print(f"Unsupported domain: {domain}")

        return ingredients

    finally:
        driver.quit()


# Example use:
if __name__ == "__main__":
    ingred = get_ingredients_from_url("http://www.geniuskitchen.com/recipe/veloute-sauce-escoffiers-recipe-469366")
    print("Ingredients:")
    for i in ingred:
        print(i)
