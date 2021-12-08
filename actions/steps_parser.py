import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from spacy import matcher
import get_recipe_json
from spacy.matcher import Matcher
import spacy

        
def parse_step_data(recipe_data):
    tools = []
    txt2list('tools_list.txt',tools)
    nlp = spacy.load('en_core_web_sm')

    cooking_verbs = []
    txt2list('cooking_verbs_list.txt',cooking_verbs)
    #print(tools)
    #find_ingredient_from_step(recipe_data['ingredients'],recipe_data['steps'])

    steps_data = []
    stop_words = ['a','to','or','and','in','read','at','room','temperature']

    time_words = ['minutes','minute','hour','hours','seconds','second']
    
    for step in recipe_data['steps']:
        step_structure = {
        'original_text':'',
        'ingredients':[],
        'tools':[],
        'methods':[],
        'cooking_time':[]
        }
        step_structure['original_text'] = step

        ingredient_set = set()
        ingredient_set.clear()

        cooking_tools_set = set()
        cooking_tools_set.clear()

        step_tokens = nltk.word_tokenize(step)
        nlp_tokens = nlp(step)
        #pos_tokens = nltk.pos_tag(step_tokens)
        for i, token in enumerate(step_tokens):
            #print(pos_tokens[i])
            #if pos_tokens[i][1] == 'VB':
            if nlp_tokens[i].lemma_.lower() in cooking_verbs:
                cooking_tools_set.add(nlp_tokens[i].lemma_.lower())
            if token.isnumeric() and i< len(step_tokens)-1 and step_tokens[i+1] in time_words:
                step_structure['cooking_time'].append(step_tokens[i] +' '+ step_tokens[i+1])

            for j, ingredient in enumerate(recipe_data['ingredients']):
                if token.isalpha() and token not in stop_words and token in ingredient['name']:
                    #print(token)
                    #print(ingredient['name'])
                    ingredient_set.add(j)
        #step_structure['ingredients'] = list(ingredient_set)
        for i in list(ingredient_set):
            step_structure['ingredients'].append(recipe_data['ingredients'][i])
        step_structure['methods'] = list(cooking_tools_set)

        #find_ingredient_from_text(step,unhealthy_ingredient_data,category_reason)
        #find_ingredient_from_text(step,healthy_ingredient_data,category_reason)

        for tool in tools:
            if tool != '' and tool.lower() in step.lower():
                step_structure['tools'].append(tool)
        #print(step_structure)
        #print(' ')
        steps_data.append(step_structure)
    return steps_data
    
def get_ingredient_str(ing_dict):
    ing_str = ''
    if ing_dict['unit'] == '':
        ing_str = ing_dict['name']
    else:
        #print('\t'+str(ing_dict['quantity']) + ' ' + ing_dict['unit']+ ' ' + ing_dict['name'])
        ing_str = str(ing_dict['quantity']) + ' ' + ing_dict['unit']+ ' ' + ing_dict['name']
    return ing_str

def print_steps_data(steps_data):
    index = 1
    for step_data in steps_data:
        print("Step "+str(index) + ":")
        print(step_data['original_text'])
        print(" ")
        if len(step_data['ingredients']) != 0:
            print("The ingredients used in this step: ")
            print(" ")
            for ing_dict in step_data['ingredients']:
                print('\t'+get_ingredient_str(ing_dict))
            print(" ")
        if len(step_data['tools'])!=0:
            print('The tools used in this step:')
            print(" ")
            for tool in step_data['tools']:
                print(tool)
            print(" ")
        if len(step_data['methods'])!=0:
            print('The methods used in this step:')
            print(" ")
            for method in step_data['methods']:
                print(method)
            print(" ")
        if len(step_data['cooking_time'])!= 0:
            print('The cooking time specified in this step:')
            print(" ")
            for ct in step_data['cooking_time']:
                print(ct)
            print(" ")
        index += 1



def find_ingredient_from_text(sentence,type_dict,reason_dict):
    for key, values in type_dict.items():
        for value in values:
            if value != '' and value in sentence.lower():
                print(reason_dict[key])
                print(value)

def txt2list(filename, newlist):
    list_dir = './knowledge_list/'
    filename = list_dir + filename
    with open(filename) as f:
        line = f.readline()
        while line:
            line = f.readline()
            newlist.append(line.strip().lower())

def build_ingredient_type_structure():

    category_reason = {
        "trans_fat":"The original recipe contains too much trans-fat, which may add your chance to get inflammation.",
        "saturated_fat":"The original recipe contains saturated fat, which may cause artery blockage.",
        "massive_sugar":"The massive amount of added sugar may higher the chance of obesity",
        "salt":"Excessive sodium consumption is the key negetive factor of longevity.",
        "vegetables":"The original recipe contains vegetables which provides you essential Vitamins and fiber, that's good for health!",
        "fruits":"Fruits appears in the orignal recipe, which is an excellent source of essential vitaminsm minerals and fiber.",
        "grains":"Grains are naturally high in fiber, helping you feel full and satisfied — which makes it easier to maintain a healthy body weight.",
        "protein":"The original recipe contains protein which is helpful for muscle gain and health.",
        "unhealthy_oil": "The original recipe uses unhealthy oil which contains trans-fat.",
        "red_meat":"Red meat contains saturated fat, which may cause artery blockage.",
        "processed_meat":"Eating processed meat increases your risk of bowel and stomach cancer. Avoid it!",
        "cheese":"Cheese also contributes saturated fat, control the daily intake!",
        "white_meat":"Original recipe contains white meat, which is wildly considered healthier than red meat.",
        "fish_meat":"Fish meat is good for health.",
        "soy_products":"Original recipe uses soy products, which are a good replacement for unhealthy meat.",
        "legume":"Original recipe contains legume, which contain antioxidants that help prevent cell damage and fight disease and aging.",
        "healthy_oil":"It's good to use healthy oil which could help the body to absorb vitamins A, D, E, and K."
    }
    massive_sugar = ['ice cream','candy','pastries','cookies','soda','fruit juices','canned fruit','processed meat','breakfast cereals','ketchup','beet sugar',\
        'blackstrap molasses','brown sugar','buttered syrup','cane juice crystals','cane sugar','caramel','carob syrup','castor sugar',\
            'coconut sugar','powdered sugar','date sugar','demerara sugar','Florida crystals','fruit juice','fruit juice concentrate','golden sugar',\
                'golden syrup','grape sugar','honey','icing sugar','invert sugar','maple syrup','molasses','muscovado sugar','panela sugar','rapadura',\
                    'raw sugar','refiner’s syrup','sorghum syrup','sucanat','treacle sugar','turbinado sugar','yellow sugar']

    unhealthy_oil = ['soybean oil','corn oil','cottonseed oil','sunflower oil','peanut oil','sesame oil','rice bran oil','flaxseed oil']
    trans_fat = ['fried food','chips','creamer','margarine']#+unhealthy_oil

    red_meat = ['beef','lamb','mutton','pork','veal','venison','goat']
    processed_meat = ['sausage','bacon','ham','deli meats','salami','pâtés','canned meat','corned beef','luncheon meats','prosciutto']
    cheese = ['cheese','roquefort cheese','camembert cheese','cotija cheese','chèvre cheese','feta cheese','mozzarella cheese','emmental cheese','cheddar cheese','gouda cheese','taleggio cheese','parmigiano-reggiano cheese','manchego cheese','monterey jack cheese']
    saturated_fat = ['coconut oil','whole milk'] #+ cheese + red_meat + processed_meat
    salt = ['salt']

    unhealthy_ingredient_data = {
        "massive_sugar":massive_sugar,
        "processed_meat":processed_meat,
        "red_meat":red_meat,
        "cheese":cheese,
        "unhealthy_oil":unhealthy_oil,
        "trans_fat":trans_fat,
        "saturated_fat":saturated_fat,
        "salt" : salt
    }


    vegetables = []
    txt2list('vegetable_list.txt',vegetables)

    fruits = []
    txt2list('fruit_list.txt',fruits)
    
    grains = ['quinoa','corn','millet','brown rice']
    healthy_oil = ['olive oil','canola oil','aocado oil','walnut oil']
    fish_meat = ['salmon','cod','herring','mahi-mahi','mackerel','perch','rainbow trout','sardines','striped bass','tuna','alaskan pollock','char']
    white_meat = ['chicken','turkey','duck','goose','game birds','rabbit','pheasant'] + fish_meat
    

    soy_products = []
    txt2list('soy_product_list.txt',soy_products)

    legume_list = []
    txt2list('legume_list.txt',legume_list)

    protein = ['egg']+legume_list+soy_products+red_meat+white_meat+fish_meat

    cooked_fresh_meat = ['boiled chicken breast','Salmon Sashimi']

    healthy_ingredient_data = {
        'vegetables':vegetables,
        'fruits':fruits,
        'grains':grains,
        'protein':protein,
        'healthy_oil':healthy_oil,
        'white_meat':white_meat,
        'fish_meat':fish_meat,
        "soy_products":soy_products,
        "legume":legume_list
    }

    health_replacement_mapping = {
        "massive_sugar":{'amount_change':0.8},
        "processed_meat":{'cooked_fresh_meat':cooked_fresh_meat},
        "red_meat":{'white_meat':white_meat},
        "cheese":{'amount_change':0.8},
        "unhealthy_oil":{"healthy_oil":healthy_oil},
        "trans_fat":{"fish_meat":fish_meat},
        "saturated_fat":{"legume":legume_list},
        "salt" : {'amount_change':0.8}
    }

    return [unhealthy_ingredient_data,healthy_ingredient_data,category_reason,health_replacement_mapping]

'''
def extract_full_name(text):
    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)
    nlp_doc = nlp(text)
    pattern = [{'POS': 'PROPN'},{'POS': 'NOUN'}]
    matcher.add('FULL_NAME', None, pattern)
    matches = matcher(nlp_doc)
    for match_id, start, end in matches:
        span = nlp_doc[start:end]
        print(span.text)
'''


def find_ingredient_from_step(ingredients_list,step_list):
    nn_ingredient = []
    for ingredient in ingredients_list:
        text = word_tokenize(ingredient['name'])
        #extract_full_name(ingredient['name'])
        pos_text = nltk.pos_tag(text)
        print(pos_text)

    for step in step_list:
        print(step)
        for ingredient in ingredients_list:
            if ingredient['name'] in step.lower():
                print(ingredient['name'])

def replace_words_in_str(replacement_list,sentence):
    #print(replacement_list)
    sentence_tokens = nltk.word_tokenize(sentence.lower())
    new_sentence = sentence
    for replacement in replacement_list:
        word_list = nltk.word_tokenize(replacement[0]['name'].lower())
        if replacement[0]['name'] != replacement[1]['name']:
            if replacement[0]['name'] in new_sentence.lower():
                new_sentence = new_sentence.replace(replacement[0]['name'],replacement[1]['name'])
            else:
                new_sentence = find_most_common_str(replacement,new_sentence)
    return new_sentence

def find_most_common_str(replacement,new_sentence):
    rptokens = nltk.word_tokenize(replacement[0]['name'])
    longest_sentence = ''
    first = True
    for i in range(len(rptokens)):
        if(rptokens[i]) in new_sentence and first:
            for j in range(len(rptokens)-i):
                if ' '.join(rptokens[i:i+j]) in new_sentence:
                    longest_sentence = ' '.join(rptokens[i:i+j])
    return longest_sentence
