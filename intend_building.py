def intend_build():

    intend_group = {}

    intend_group['greet'] = [
        'Hi',
        'Hello'
    ]
    intend_group['get_recipe'] = [
        'Walk me through a recipe from AllRecipes.com.'
    ]
    intend_group['send_url'] = [
    'https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/'
    ]
    intend_group['specific_how_to'] = [
        'How do I <specific technique>?',
    ]

    intend_group['specific_what_is'] = [
        'What is a <tool being mentioned>?',
    ]

    intend_group['vague_how_to'] = [
        'How do I do that?',
        'Hello'
    ]
    intend_group['get_ingredient_amount_of_current_step'] = [
        'How much of <ingredient> do I need?'
    ]
    intend_group['get_temperature_of_current_step'] = [
        'What temperature?',
        'Hello'
    ]
    intend_group['get_time_of_current_step'] = [
        'How long do I <specific technique>?',
        'Hello'
    ]
    intend_group['get_ingredient_substitution'] = [
        'What can I substitute for <ingredient>?',
        'Hello'
    ]
    return intend_group

