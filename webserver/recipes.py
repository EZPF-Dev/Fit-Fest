import requests
from bs4 import BeautifulSoup

def search_recipes(ingredients, exclude=[], cuisine=''):
    """
    This function searches for recipes on Allrecipes.com based on the given ingredient criteria, excluding any
    recipes that contain any of the excluded ingredients and filtering by the specified cuisine type (if any).
    """
    url = 'https://www.allrecipes.com/search/results/?wt={}&sort=re&page={}&pht={}'
    recipes = []
    page_number = 1
    while True:
        print("asking")
        res = requests.get(url.format(ingredients, page_number, cuisine))
        print(res)
        soup = BeautifulSoup(res.content, 'html.parser')
        results = soup.find_all('article', {'class': 'fixed-recipe-card'})
        if not results: # no more results, break out of the loop
            break
        print(results)
        for result in results:
            recipe = {}
            recipe['name'] = result.find('h3', {'class': 'fixed-recipe-card__h3'}).text.strip()
            recipe['rating'] = result.find('span', {'class': 'stars'}).attrs['data-ratingstars']
            recipe['url'] = result.find('a', {'class': 'fixed-recipe-card__title-link'}).attrs['href']
            recipe['ingredients'] = result.find('div', {'class': 'fixed-recipe-card__ingredients'}).text.strip()
            # check if any excluded ingredients are present in the recipe
            excluded = False
            for exc in exclude:
                if exc in recipe['ingredients']:
                    excluded = True
                    break
            # check if the recipe's cuisine type matches the specified cuisine (if any)
            if cuisine:
                ct = result.find('span', {'class': 'fixed-recipe-card__category'})
                if not ct or cuisine.lower() not in ct.text.lower():
                    continue
            if not excluded:
                recipes.append(recipe)
        page_number += 1
    return recipes

# example usage:
ingredients = 'chicken, rice, broccoli'
exclude = ['onion', 'garlic']
cuisine = 'chinese'
print("rPrinting")
recipes = search_recipes(ingredients, exclude, cuisine)
for recipe in recipes:
    print(recipe['name'])
    print(recipe['rating'])
    print(recipe['url'])
    print(recipe['ingredients'])
    print()
