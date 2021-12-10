import get_recipe_json
import steps_parser
import intend_building
import difflib
import os

'''
Basic goals:

Y1. Recipe retrieval and display (see example above, including "Show me the ingredients list");
Y2. Navigation utterances ("Go back one step", "Go to the next step", "Repeat please", "Take me to the 1st step", "Take me to the n-th step");
N3. Vague "how to" questions ("How do I do that?", in which case you can infer a context based on what's parsed for the current step);
Y4. Specific "how to" questions ("How do I <specific technique>?");
Y5. Simple "what is" questions ("What is a <tool being mentioned>?");
N6. Asking about the parameters of the current step ("How much of <ingredient> do I need?", "What temperature?", "How long do I <specific technique>?", "When is it done?");
N7. Ingredient substitution questions ("What can I substitute for <ingredient>?");
Y8. Name your bot :)

'''
intend_group = intend_building.intend_build()
bot_name = "JJK Bot: "
context = {}

def data_init(url):
    global recipe_data 
    global step_data
    recipe_data = get_recipe_json.get_recipe_json(url)
    step_data = steps_parser.parse_step_data(recipe_data)
    #return [recipe_data,step_data]
    print(step_data)
    context.clear()


def get_intend(sentence):
    intend_key = []
    for intend, eglist in intend_group.items():
        intends = difflib.get_close_matches(sentence,eglist)
        if len(intends) != 0:
            #print(intends)
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

def get_all_ingredients():
    print(bot_name+'Here are the ingredients for \"'+recipe_data['name'] +'\" :')
    for ingDict in recipe_data['ingredients']:
        print(str(ingDict['quantity'])+' '+ingDict['unit']+' '+ingDict['name'])

def go_to_nth_step(input_str):
    for c in input_str:
        if c.isnumeric():
            step = int(c)
            if 0 <step<= len(step_data):
                context['curr_step'] = step
                print(bot_name+'The step '+c+' is: '+step_data[step-1]['original_text'])
            else:
                print(bot_name+'Sorry. There are only '+str(len(step_data))+' steps in the recipe, please specify a correct step.')

def response(intend,input_str,context):
    if intend == 'greet':
        print(bot_name+"Hi, how can I help you?")
        context['last_response'] = 'greet'

    elif intend == 'get_recipe':
        print(bot_name+'Sure. Please specify a URL.')
        context['last_response'] = 'get_recipe'

    elif intend == 'send_url':
        data_init(input_str)
        print(bot_name+'Alright. So let\'s start working with '+ recipe_data['name'] +'. What do you want to do?')
        context['last_response'] = 'send_url'
        print(bot_name+'[1] Go over ingredients list or [2] Go over recipe steps.')
    
    elif intend == 'select_option':
        if context['last_response'] == 'send_url':
            context['curr_branch'] = input_str
            if input_str == '1':
                get_all_ingredients()
            elif input_str == '2':
                go_to_nth_step('1')
        else:
            intend = ''
            response(intend,input_str,context)

    elif intend == 'specific_how_to':
        query_url = answer_specific(input_str)
        print(bot_name+ 'No worries. I found a reference for you: '+query_url)

    elif intend == 'specific_what_is':
        query_url = answer_specific(input_str)
        print(bot_name+ 'No worries. I found a reference for you: '+query_url)

    elif intend == 'back_one_step':
        if context['curr_step'] == 1:
            print(bot_name+'Sorry, this is already the first step.')
        else:
            go_to_nth_step(str(context['curr_step']-1))
    
    elif intend == 'forward_one_step':
        if context['curr_step'] == len(step_data):
            print(bot_name+'Sorry, there is no next step. This is already the last step.')
        else:
            go_to_nth_step(str(context['curr_step']+1))

    elif intend == 'goto_specific_step':
        go_to_nth_step(input_str)

    elif intend == 'repeat_current_step':
        go_to_nth_step(str(context['curr_step']))

    elif intend == 'get_time_of_current_step':
        if len(step_data[context['curr_step']-1]['cooking_time'])>0:
            print(bot_name+'It is done after '+step_data[context['curr_step']-1]['cooking_time'][0])
        else:
            print(bot_name+'Sorry, I don\'t know how long you should do based on the provided recipe.')

    elif intend == 'get_temperature_of_current_step':
        if len(step_data[context['curr_step']-1]['cooking_temp'])>0:
            print(bot_name+'You need '+step_data[context['curr_step']-1]['cooking_temp'][0])
        else:
            print(bot_name+'Sorry, I don\'t know what temperature you should heat based on the provided recipe.')

    elif intend == 'vague_how_to':
        if len(step_data[context['curr_step']-1]['methods'])>0:
            intend = 'specific_how_to'
            input_str = 'How to '+ step_data[context['curr_step']-1]['methods'][0]
            print(bot_name+ 'Now I will search for question \"'+input_str+'\" for you in Internet.')
            response(intend,input_str,context)
        else:
            print(bot_name+'Sorry, I don\'t know what do you refer to, please ask specifically.')


    else:
        print(bot_name+"Sorry. I can't understand you for now. Could you please change another question?")
    '''
    
    
    elif intend == 'get_ingredient_amount_of_current_step':
    
    elif intend == 'get_ingredient_substitution':
    '''
    
   

# now, to clear the screen
if __name__ == "__main__":
    os.system('cls' if os.name=='nt' else 'clear')

    #intend = get_intend('https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/')
    #print(intend)
    #data_init('https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/')


    print('Welcome to talk with JJK(Jipeng_Josh_Komal) Recipe Bot!')
    print('You can type whatever you want to chat with JJK, type \'q\' to quit the dialog.')
    print('')
    while(1):
        input_str = input("You: ")
        if input_str == 'q':
            break
        print('')
        intend = get_intend(input_str)
        if len(intend) != 0:
            intend = intend[0]
        response(intend,input_str,context)
        #print(intend)
        print('')

