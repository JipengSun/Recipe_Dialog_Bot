import get_recipe_json
import steps_parser
import intend_building
import difflib
import os

intend_group = intend_building.intend_build()
bot_name = "JJK Bot: "
context = {}

def data_init(url):
    global recipe_data 
    global step_data
    recipe_data = get_recipe_json.get_recipe_json(url)
    step_data = steps_parser.parse_step_data(recipe_data)
    #return [recipe_data,step_data]


def get_intend(sentence):
    intend_key = []
    for intend, eglist in intend_group.items():
        intends = difflib.get_close_matches(sentence,eglist)
        if len(intends) != 0:
            print(intends)
            intend_key.append(intend)
    return intend_key

def answer_specific(input_str):
    input = input_str.lower()
    a=input.split()
    a = '+'.join(a)
    a = a.replace("?","")
    base_url = 'https://www.youtube.com/results?search_query='
    final_url = base_url + a
    return final_url

def response(intend,input_str,context):
    if intend == 'greet':
        print(bot_name+"Hi, how can I help you?")
    elif intend == 'get_recipe':
        print(bot_name+'Sure. Please specify a URL.')
    elif intend == 'send_url':
        data_init(input_str)
        print(bot_name+'Alright. So let\'s start working with '+ recipe_data['name'] +'. What do you want to do?')
    elif intend == 'specific_how_to':
        query_url = answer_specific(input_str)
        print(bot_name+ 'No worries. I found a reference for you: '+query_url)
    elif intend == 'specific_what_is':
        query_url = answer_specific(input_str)
        print(bot_name+ 'No worries. I found a reference for you: '+query_url)
    else:
        print(bot_name+"Sorry. I can't understand you for now. Could you please change another question?")
    '''
    
    elif intend == 'vague_how_to':
    elif intend == 'get_ingredient_amount_of_current_step':
    elif intend == 'get_temperature_of_current_step':
    elif intend == 'get_time_of_current_step':
    elif intend == 'get_ingredient_substitution':
    elif intend == 'forward_one_step':
    elif intend == 'back_one_step':
    elif intend == 'goto_specific_step':
    elif intend == 'repeat_current_step':
    '''
    
   

# now, to clear the screen
if __name__ == "__main__":
    os.system('cls' if os.name=='nt' else 'clear')

    intend = get_intend('https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/')
    print(intend)
    data_init('https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/')


    print('Welcome to talk with JJK Recipe Bot!')
    print('You can type whatever you want to chat with JJK, type \'q\' to quit the dialog.')
    while(1):
        input_str = input("You: ")
        if input_str == 'q':
            break
        intend = get_intend(input_str)
        if len(intend) != 0:
            intend = intend[0]
        response(intend,input_str,context)
        print(intend)

