import nltk
import get_recipe_json
import steps_parser
import intend_building
import difflib
import os

'''
Basic goals:

Y1. Recipe retrieval and display (see example above, including "Show me the ingredients list");
Y2. Navigation utterances ("Go back one step", "Go to the next step", "Repeat please", "Take me to the 1st step", "Take me to the n-th step");
Y3. Vague "how to" questions ("How do I do that?", in which case you can infer a context based on what's parsed for the current step);
Y4. Specific "how to" questions ("How do I <specific technique>?");
Y5. Simple "what is" questions ("What is a <tool being mentioned>?");
Y6. Asking about the parameters of the current step ("How much of <ingredient> do I need?", "What temperature?", "How long do I <specific technique>?", "When is it done?");
Y7. Ingredient substitution questions ("What can I substitute for <ingredient>?");
Y8. Name your bot :)

'''
intend_group = intend_building.intend_build()
bot_name = "JJK Bot: "
context = {'recipe_specified':False}
stop_words = ['i','of','do']

def data_init(url):
    global recipe_data 
    global step_data
    recipe_data = get_recipe_json.get_recipe_json(url)
    step_data = steps_parser.parse_step_data(recipe_data)
    #return [recipe_data,step_data]
    #print(step_data)
    context.clear()


def get_intend(sentence):
    intend_key = []
    similarity_dict = {}
    for intend, eglist in intend_group.items():
        score_list = []
        for eg in eglist:
            editdist = nltk.edit_distance(sentence.lower(),eg.lower())
            score_list.append(float(editdist/len(sentence)))
            #print(eg,float(editdist/len(sentence)))
        #print(score_list)
        minscore = min(score_list)
        similarity_dict[intend] = minscore
    minkey = min(similarity_dict,key = lambda k: similarity_dict[k])
    #print(similarity_dict)
    if (similarity_dict[minkey]<0.6):
        intend_key.append(minkey)
    return intend_key

def answer_specific(input_str):
    input = input_str.lower()
    a=input.split()
    a = '+'.join(a)
    a = a.replace("?","")
    base_url = 'https://www.google.com/results?search_query='
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
    need_recipe_first = ['select_option','get_all_ingredients','confirm','back_one_step','forward_one_step','goto_specific_step','repeat_current_step','get_time_of_current_step','get_temperature_of_current_step',\
        'vague_how_to','get_ingredient_amount_of_current_step']
    if intend in need_recipe_first and context['recipe_specified']:
        if intend == 'select_option':
            if context['last_response'] == 'send_url':
                context['curr_branch'] = input_str
                if input_str == '1':
                    get_all_ingredients()
                elif input_str == '2':
                    go_to_nth_step('1')
            else:
                intend = ''
                response(intend,input_str,context)
        elif intend == 'get_all_ingredients':
            get_all_ingredients()
        elif intend == 'confirm':
            #print(context['last_response'])
            if context['last_response'] == 'appreciation':
                go_to_nth_step(str(context['curr_step']+1))
            else:
                print("Is there anything else I can help you with")
                context['last_response'] = 'appreciation'
                
            

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
        
        elif intend == 'get_ingredient_amount_of_current_step':
            answered = False
            wt = nltk.word_tokenize(input_str.lower())
            for token in wt:
                if token not in stop_words:
                    for ig in recipe_data['ingredients']:
                        if token in ig['name'] and not answered:
                            #print(token,ig['name'])
                            print(bot_name+'You need '+str(ig['quantity']) + ' '+ig['unit']+' '+ig['name'])
                            answered = True
            if not answered:
                print(bot_name+'Sorry I can\'t find the ingredient you specified is used in this step.')

        elif intend == 'get_ingredient_substitution':
            answered = False
            wt = nltk.word_tokenize(input_str.lower())
            for token in wt:
                if token not in stop_words:
                    for ig in recipe_data['ingredients']:
                        if token in ig['name'] and not answered:
                            #print(token,ig['name'])
                            print(bot_name+'I will search in Internet for suitable substitution of '+ ig['name'])
                            input_str = 'What can I substitute for '+ig['name']
                            intend = 'specific_what_is'
                            response(intend,input_str,context)
                            answered = True
            if not answered:
                print(bot_name+'Sorry I can\'t find the ingredient you specified is used in this step.')


        else:
            print(bot_name+"Sorry. I didn't understand you. Could you please ask another question or try rephrasing your last one?")
    else:
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
            context['recipe_specified'] = True
            print(bot_name+'[1] Go over ingredients list or [2] Go over recipe steps.')

        elif intend == 'appreciation':
            if 'curr_step' in context.keys():
                if context['curr_step'] != len(step_data):
                    print(bot_name+'You are welcome. Should I continue to step ' + str(context['curr_step']+1) + ' ?')
                    context['last_response'] = 'appreciation'
                else:
                    print(bot_name+ 'You are welcome. You have finished the recipe steps. You can ask more questions.')
            else:
                print(bot_name+'Thank you. What can I do for you?')

        elif intend == 'specific_how_to':
            query_url = answer_specific(input_str)
            print(bot_name+ 'No worries. I found a reference for you: '+query_url)

        elif intend == 'specific_what_is':
            query_url = answer_specific(input_str)
            print(bot_name+ 'No worries. I found a reference for you: '+query_url)
        else:
            print(bot_name+'I don\'t know what you mean for now. Or could you please tell me the recipe URL first?')
    
   

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
        # print(intend)
        if len(intend) != 0:
            intend = intend[0]
        response(intend,input_str,context)
        print('')

'''
<USER STORY>

User: Walk me through a recipe from AllRecipes.com.

Bot: Sure. Please specify a URL.

User: https://www.allrecipes.com/recipe/218091/classic-and-simple-meat-lasagna/ (Links to an external site.)

Bot: Alright. So let's start working with "Classic and Simple Meat Lasagna." What do you want to do?

Bot: [1] Go over ingredients list or [2] Go over recipe steps.

User: 2.

Bot: The 1st step is: Preheat oven to 350 degrees F (175 degrees C).

User: How do I preheat the oven?

Bot: No worries. I found a reference for you: https://www.youtube.com/results?search_query=how+to+preheat+oven (Links to an external site.)

User: Thanks!

Bot: Should I continue to the 2nd step?

User: Show me the ingredients list.

Bot: Here are the ingredients for "Classic and Simple Meat Lasagna":

12 whole wheat lasagna noodles

1 pound lean ground beef

(...)

1 1/2 25 ounce jars tomato-basil pasta sauce

2 cups mozzarella cheese, shredded

User: Thanks again!

Bot: Should I continue to the 2nd step?

User: Yes, please.

Bot: (...)

</USER STORY>
'''