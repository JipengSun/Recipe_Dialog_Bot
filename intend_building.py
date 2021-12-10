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
        'How do I do that?'
    ]
    intend_group['get_ingredient_amount_of_current_step'] = [
        'How much of <ingredient> do I need?'
    ]
    intend_group['get_temperature_of_current_step'] = [
        'What temperature?'
    ]
    intend_group['get_time_of_current_step'] = [
        'How long do I <specific technique>?'
    ]
    intend_group['get_ingredient_substitution'] = [
        'What can I substitute for <ingredient>?'
    ]
    intend_group['forward_one_step'] = [
        'Go to the next step'
    ]
    intend_group['back_one_step'] = [
        'Go back one step',
        'Previous step'
    ]
    intend_group['goto_specific_step'] = [
        'Take me to the n-th step'
    ]
    intend_group['repeat_current_step'] = [
        'Repeat please'
    ]
    return intend_group

