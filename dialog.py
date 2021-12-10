import get_recipe_json
import steps_parser
import intend_building
import difflib

intend_group = intend_building.intend_build()

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


if __name__ == "__main__":
    intend = get_intend('https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/')
    print(intend)
    data_init('https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/')
    end = False
    print('Welcome to talk with JJK Recipe Bot!')
    print('You can type whatever you want to chat with JJK, type \'q\' to quit the dialog.')
    while(not end):
        input_str = input("You: ")
        if input_str == 'q':
            end = True
            break
        intend = get_intend(input_str)
        print(intend)

