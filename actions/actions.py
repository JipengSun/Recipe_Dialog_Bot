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


def get_ingredient_list():
    return

def navigate_utterances(curr_step,instruction):
    # curr_step int
    # instruction str
    next_step = 0

    return next_step

def vague_how_to():
    # OH
    return

def specific_qestion(question):
    url = ''
    return url

def get_ingredient_quantity():
    return

def get_temperature():
    return

def get_time():
    return

def get_substitude():
    return
