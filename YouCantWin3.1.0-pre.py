from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

import unicodedata

import time

import requests


def remove_unwanted_tags(text):
    return text.replace('&nbsp;', ' ').replace('&lt', ' ').replace('&gt', ' ').replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '').replace('  ', ' ').replace('   ', ' ').replace('     ', ' ')
 


def normalize_text(text):
    # Normalize to NFD (decomposing characters with accents)
    text = unicodedata.normalize('NFD', text)
    
    # Remove combining characters (accents, tildes)
    text = ''.join(char for char in text if not unicodedata.combining(char))
    
    # Lowercase and strip whitespace
    return text.strip().lower()


def get_answers_dictionary(id):
    """
        Get the details of a game from the Kahoot API.
    """
    response = requests.get('https://play.kahoot.it/rest/kahoots/' + id)

    # Dictionary to store question-answer pairs
    question_answers = {}  

    if response.status_code == 200:

        # Store the answer provided by the API in a Python dictionary
        json_answer = response.json()

        # Check if there is a field named 'questions' inside the JSON response
        if 'questions' in json_answer:

            # Store all questions in a separate variable
            questions = json_answer['questions']

            # Iterate through each question
            for question in questions:

                # Store all of the choices per question
                choices = question['choices']

                # Iterate through each choice 
                for choice in choices:

                    # Check if the choice's answer is True
                    if choice['correct']:
                        
                        # If the answer is true, store the question-answer pair
                        question_answers[question['question']] = choice['answer']

    else:
        print('Error code:', response.status_code)
        return None

    return question_answers


def get_answers_from_local_dictionary():
    # Initialize an empty dictionary to store question-answer pairs
    answers = {}

    # Open the file in read mode with UTF-8 encoding
    with open('LatestKahootsQuestions.txt', 'r', encoding='UTF-8') as f:
        # Iterate through each line in the file
        for line in f:
            # Strip any extra whitespace or newline characters from the line
            line = line.strip()

            # Split the line into question and answer based on the delimiter
            if ' -|@|- ' in line:
                question, answer = line.split(' -|@|- ', 1)

                # Add the question-answer pair to the dictionary
                answers[question] = answer

    # Return the dictionary containing all question-answer pairs
    return answers


# game_id = input("Game ID > ")
game_pin = input("Game Pin > ")

my_dictionary = get_answers_from_local_dictionary()

if my_dictionary:
    print(f"Data stored correctly")
    print(f"Questions in the dictionary: {len(my_dictionary)}")
else:
    print("NONONO")
    exit(1)
        
driver = webdriver.Firefox()

full_url = 'https://kahoot.it/?pin=' + game_pin + '&refer_method=link'

driver.get(full_url)

driver.set_window_size(1280, 720)

question = None # Store the current question
answers = []    # Store the answers

QUESTION_BEFORE_ANSWERS_CLASS_NAME = 'block-title__Title-sc-1kt4e1p-0'                  # Class name for the question that appears BEFORE the answers are shown
QUESTION_WHILE_ANSWERS_CLASS_NAME = 'extensive-question-title__Title-sc-1m88qtl-0'      # Class name for the question that appears WHILE  the answers are shown

ANSWER_CLASS_NAME = 'choice__Choice-sc-ym3b8f-4'

while True:

    # Store elements
    elements = driver.find_elements(By.CLASS_NAME, QUESTION_BEFORE_ANSWERS_CLASS_NAME)

    # If there's a matching element, it's the question, store it
    question = elements[0].text if len(elements) > 0 else None
        
    # In case the question couldn't be found, look for the question that appears
    # while the answers are shown
    if question is None:

        # Look for the question in question (haha)
        elements = driver.find_elements(By.CLASS_NAME, QUESTION_WHILE_ANSWERS_CLASS_NAME)

        # Store the text of it
        question = elements[0].text if len(elements) > 0 else None

    # Look for answers only if there's a question stored
    if question is not None:

        try:

            question = normalize_text(question)

            question = remove_unwanted_tags(question)

            # Store the expected answer to look for
            expected_answer = my_dictionary[question]

            # Normalize the expected answer (remove accents, strip, and convert to lowercase)
            normalized_expected_answer = normalize_text(expected_answer)

            print(f'Expected answer: "{normalized_expected_answer}"')

            loop = True

            try:

                print("Ready to Answer")

                while loop:

                    # Get the answers on screen
                    answers = driver.find_elements(By.CLASS_NAME, ANSWER_CLASS_NAME)

                    # Iterate over each element found
                    for answer in answers:
                        
                        # Normalize the answer text (remove accents, strip, and convert to lowercase)
                        normalized_answer = normalize_text(answer.text)

                        # Check if the normalized answer text matches the normalized expected answer
                        if normalized_answer == normalized_expected_answer:
                            
                            # Debug
                            print(f"Correct answer     '{answer.text}'")
                            print(f"found for question '{question}'")

                            # Remove entry from the dictionary
                            my_dictionary.pop(question)

                            loop = False
                            question = None

                            try:
                                # Click 5 times, just to make sure
                                for i in range(5):
                                    answer.click()
                            except StaleElementReferenceException:
                                # The button is now gone, do nothing about it
                                continue

                            # Exit both the for loop and the while loop
                            question = None
                            loop = False
                            break  

                    # Just for debugging, don't need delay
                    # time.sleep(1)

            except StaleElementReferenceException:
                print("Elements disappeared. exception catched")
        
        except KeyError as e:
            print(f'Question {e} not found in the dictionary')
            time.sleep(1)
            
        question = None
