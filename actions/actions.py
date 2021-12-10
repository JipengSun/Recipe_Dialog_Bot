# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# from actions.steps_parser import parse_step_data
import get_recipe_json
import steps_parser

class Recipe:
    #be sure to use Recipe.parse_recipe() when you create a recipe
    def __init__(self, url):
        self.url = url
        self.steps = ""
        self.data = ""
        # self.ingredients = []
        self.current_step = 0
    
    def parse_recipe(self):
        self.data = get_recipe_json.get_recipe_json(self.url)
        self.steps = steps_parser.parse_step_data(self.data)

    # def get_recipe_data(self):
    #     return self.data

    def navigate(self, direction, target = None):
        #direction = +1 or -1
        if target == None:
            self.current_step += direction
        else: 
            self.current_step = target

    def get_ingredient_list(self):
        ingList = []
        for ing in self.data['ingredients']:
            ingList.append(ing['name'])
        return ingList

    def get_ingredient_quantity(self, ingredient):
        ingList = self.get_ingredient_list()
        for ing in range(len(ingList)):
            if ingredient in ingList[ing]:
                return str(self.data['ingredients'][ing]['quantity']) + " " + str(self.data['ingredients'][ing]['unit'])
        return "Ingredient not found."




    def get_time(self):
        if self.steps[self.current_step]['cooking_time'] == []:
            return "There is no relavant time to return"
        else:
            return "Cooking time is " + self.steps[self.current_step]['cooking_time'][0] + "."

##



def vague_how_to():
    # OH
    return

def specific_qestion(question):
    url = ''
    return url

def get_temperature():
    return
    
def get_substitute(ingredient):
    search = "https://www.google.com/search?q=what+can+i+substitute+for+" + str(ingredient)
    

url1 = 'https://www.allrecipes.com/recipe/172060/hummus-and-prosciutto-wrap/'
# print(get_time(url1,1))
r1 = Recipe(url1)
r1.parse_recipe()
r1.navigate(1)
print(r1.get_ingredient_quantity('prosciutto'))
