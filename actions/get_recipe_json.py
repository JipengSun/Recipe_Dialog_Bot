import requests
from bs4 import BeautifulSoup
import json
import pprint

url1 = 'https://www.allrecipes.com/recipe/172060/hummus-and-prosciutto-wrap/'
url2 = 'https://www.allrecipes.com/recipe/143809/best-steak-marinade-in-existence/'
url3 = 'https://www.allrecipes.com/recipe/150273/spicy-pimento-cheese-sandwiches-with-avocado-and-bacon/'

def get_recipe_json(url):

    strhtml=requests.get(url)
    soup=BeautifulSoup(strhtml.text,'lxml')

    raw_result = {}

    raw_result['name'] = soup.select('body > div.docked-sharebar-content-container > div > main > div.recipe-container.two-col-container > div.content.two-col-main-content.karma-content-container > div.recipe-content.two-col-content.karma-main-column > div.main-header.recipe-main-header > div.intro.article-info > div > h1')[0].get_text()
    raw_result['intro'] = soup.select('body > div.docked-sharebar-content-container > div > main > div.recipe-container.two-col-container > div.content.two-col-main-content.karma-content-container > div.recipe-content.two-col-content.karma-main-column > div.main-header.recipe-main-header > div.recipe-summary > p')[0].get_text()
    raw_result['meta'] = soup.select('body > div.docked-sharebar-content-container > div > main > div.recipe-container.two-col-container > div.content.two-col-main-content.karma-content-container > div.recipe-content.two-col-content.karma-main-column > div.two-col-content-wrapper > div.recipe-content-container > div.lead-content-wrapper.two-col-style > div.lead-content-aside-wrapper.video-with-tout-image > div > section > div')#.find_all('div',{'class': 'recipe-meta-item-body'})
    raw_result['ingredients'] = soup.select('body > div.docked-sharebar-content-container > div > main > div.recipe-container.two-col-container > div.content.two-col-main-content.karma-content-container > div.recipe-content.two-col-content.karma-main-column > div.two-col-content-wrapper > div.recipe-content-container > div.recipe-shopper-wrapper > section.component.recipe-ingredients.recipeIngredients.container.interactive > fieldset > ul')[0].find_all('input')
    raw_result['step'] = soup.select('body > div.docked-sharebar-content-container > div > main > div.recipe-container.two-col-container > div.content.two-col-main-content.karma-content-container > div.recipe-content.two-col-content.karma-main-column > div.two-col-content-wrapper > div.recipe-content-container > section.component.recipe-instructions.recipeInstructions.container > fieldset > ul')[0].find_all('p')

    recipe_data = {
        "name":raw_result['name'],
        "ingredients":[],
        "steps":[]
    }

    for item in raw_result['ingredients']:
        ingredient_data = {}
        if item['data-init-quantity'] != '':
            ingredient_data['quantity'] = float(item['data-init-quantity'])
        else:
            ingredient_data['quantity'] = 1
        ingredient_data['unit'] = item['data-unit']
        ingredient_data['name'] = item['data-ingredient']
        recipe_data['ingredients'].append(ingredient_data)

    for step in raw_result['step']:
        recipe_data['steps'].append(step.get_text())

    recipe_json = json.dumps(recipe_data)

    return recipe_data
    #print(recipe_json)

    with open('./raw_recipe.json', 'w') as json_file:
     json.dump(recipe_json, json_file)


    with open('./raw_recipe.json') as f:
     data = json.load(f)

    return data


#print(get_recipe_json(url3))