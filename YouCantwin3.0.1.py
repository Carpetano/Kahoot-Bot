"""



▄██   ▄    ▄██████▄  ███    █▄   ▄████████    ▄████████ ███▄▄▄▄       ███      ▄█     █▄   ▄█  ███▄▄▄▄   
███   ██▄ ███    ███ ███    ███ ███    ███   ███    ███ ███▀▀▀██▄ ▀█████████▄ ███     ███ ███  ███▀▀▀██▄ 
███▄▄▄███ ███    ███ ███    ███ ███    █▀    ███    ███ ███   ███    ▀███▀▀██ ███     ███ ███▌ ███   ███ 
▀▀▀▀▀▀███ ███    ███ ███    ███ ███          ███    ███ ███   ███     ███   ▀ ███     ███ ███▌ ███   ███ 
▄██   ███ ███    ███ ███    ███ ███        ▀███████████ ███   ███     ███     ███     ███ ███▌ ███   ███ 
███   ███ ███    ███ ███    ███ ███    █▄    ███    ███ ███   ███     ███     ███     ███ ███  ███   ███ 
███   ███ ███    ███ ███    ███ ███    ███   ███    ███ ███   ███     ███     ███ ▄█▄ ███ ███  ███   ███ 
 ▀█████▀   ▀██████▀  ████████▀  ████████▀    ███    █▀   ▀█   █▀     ▄████▀    ▀███▀███▀  █▀    ▀█   █▀  
                                                                                                         



"""
from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

from fuzzywuzzy import fuzz

import time

import requests
import threading

import os
from os import system

"""
# # # # # # # # # # # # #  UPDATE NOTES  # # # # # # # # # # # # # 

                            1.0.0
        Print all answers by getting the kahoot id.

                            2.0.0
        Fully Automated Playing and Log-in processeses even while 
        in the background.

        Play by just entering kahoot info inside a dedicated vm.

                        2.0.1 - 2.0.4
        Migrated dedicated vm to independent selenium firefox browsers
        allowing to have multiple instances run independently of each
        other even while minimized.

                            2.1.0
        Replaced in-game coordinates to work on kahoots with the option 
         "see questions on player's screen" is turned on.

        Also optimized cursor position so it get's mostly 1000 points.
        (1st question gets 980+/- points, don't know why)

        Added comments everywhere.

                            2.1.1
        Slightly moved pixel color detection since larger questions caused
        it to read wrong colors, thus making it never answer.

        Also increased a bit the distance of the cursor travel since if the
        answer was long and green it wouldn't click it skipping the question 
        and answering one question ahead completely messing up with the index.

        ALSO added the possibility to know it's time to answer if that pixel is 
        blue since for some reason a true or false question in "jujofutbol" 
        reversed the colors making it not work, I hope this works...
        what the absolute fu-.

                            2.2.0
        Removed the screenshot question detection and cursor positioning, 
        replaced with find_elements improving reliability, efficiency and speed
        making it get 1000 points more often using less resources
        (although it needs try catches)

                            2.3.0
        Replaced ALL pixel-position-clicking stuff and replaced with find_elements
        making it much faster and allowing for a smaller window (skin setting)

                            2.3.1
        Added name length check.
        Allow the bot to play on loop in case game is set to automatic play.

                            2.3.2
        Removed skin selection.
        It only causes problems not making it play, therefore it's gone for good.
        Rather for it to play with a random skin than not play at all.
        
        


# # # # # #  ¿FUTURE UPDATES?  # # # # # #         

==== Done ====

-Automatically detect if "see questions on player's screen" is on and modify 
 coordinates to play accordingly (Fixed ver: 2.2.0)

-Make the first answer get 1000 points aswell (Probably fixed ver: 2.2.0)

-Remove magic number delays inside the login screen + skin selection (fixed ver: 2.3.0)

-Make skin selection by scanning screen and not fully pre-defined moves (fixed ver: 2.3.0)

-Make window smaller so it takes less space (fixed ver: 2.3.0 ; 500x500 works fine)

-Make it loop if game is in autoplay and it loops (fixed ver: 2.3.1)

-Adding a 15 character max in name (fixed ver: 2.3.1)

-Circumvent randomized question / answer positions by performing OCR or getting html code (pls no, I dont wanna have to scan for question then locate answers zzzz :c) (fixed ver: 3.0.1)

==== WIP ====

-Get the kahoot id by just entering the game id (probably not possible, unless scanning for packages or something)


"""

version = '3.0.1'

# Change window title
system("title " + 'YouCantWin ' + version)


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
                        # print(f"Q: {question['question']}")
                        # print(f"A: {choice['answer']}\n")

    else:
        print('Error code:', response.status_code)

    return question_answers


def join_lobby(driver, pin, player_name):
    """
       Join a lobby using the provided driver, pin number and player name.
    """
    # Get new kahoot game id and directly join so it only asks for name
    full_url = 'https://kahoot.it/?pin=' + pin + '&refer_method=link'

    # Replace 'your_url_here' with the actual URL of the webpage containing the button
    driver.get(full_url)

    # Set window size
    driver.set_window_size(500,500)

    # Variables for the loops below
    nick = False
    join_game = False

    menu = False
    skin = False
    accesory = False
    accessory_tab = False
    done_button = False

    # Fill in the nickname and click the submit button
    while not nick:

        # Add some delay
        time.sleep(0.1)

        # Store the edit skin button location
        button_xpath = "//input[@name='nickname' and @data-functional-selector='username-input']"

        # Locate the button
        buttons = driver.find_elements('xpath', button_xpath)

        for button in buttons:
            button.send_keys(player_name)
            nick = True
            # print('Nickname entered')

    # Fill in the nickname and click the submit button
    while not join_game:

        # Add some delay
        time.sleep(0.1)

        # Store the edit skin button location
        button_xpath = "//button[@class='button__Button-sc-vzgdbz-0 fyUZin nickname-form__SubmitButton-sc-1mjq176-1 dPDKgw' and @data-functional-selector='join-button-username']"

        # Locate the button
        buttons = driver.find_elements('xpath', button_xpath)

        for button in buttons:
            button.click()
            join_game = True
            # print('Joining Game')

# Get Game data
while True:

    # Ask user to enter the kahoot id 
    game_id = input("Enter the game ID > ")

    # Clear terminal so the id is not visible
    os.system('cls')

    # Ask user to enter the game pin
    game_pin = input("Enter the game pin > ")

    # Fetch the questions and store it in a list
    question_answers = get_answers_dictionary(game_id)

    if question_answers:
        break
    else:
        print('no data found')

# Clear terminal
os.system('cls')

player_name = 'xxxxxxxxxxxxxxxxxxxx'

while len(player_name) > 15:

    # Ask user to enter the player name
    player_name = input(f'Enter the desired name (leave blank for YouCantWin {version[:3]}) Maximum 15 characters > ')

    # Clear terminal
    os.system('cls')

    if len(player_name) > 15:
        print('Max characters: 15') 

# In case there's no player name, default it to YouCantWin version
if(player_name == ""):
    player_name = "YouCantWin " + version[:3] # This makes it so it takes the first 3 characters only

# Print match data
print(f'Playing as: {player_name}')    
# print(f'Number of Questions: {len(get_answers_dictionary)}')

# Initialize firefox window
driver = webdriver.Firefox()

# Join the game
actions = ActionChains(driver)

# Join and set the skin
join_lobby(driver, game_pin, player_name)

# Surround infinite gaming loop
while True:

    game_finished = False

    print('Ready')

    # Game loop
    while not game_finished:

        stored = False
        question_answered = False

        try:

           # Look at the window title until the question is found in the dictionary
            while not stored:
                temp_title = driver.title

                # Extract the possible question from the title
                possible_question = temp_title.split(' - Kahoot!')[0].strip()

                # Initialize variables to store the best matching question and its corresponding answer
                best_match = None
                best_score = -1

                # Iterate through the questions in question_answers dictionary and find the best match
                for question, answer in question_answers.items():
                    score = fuzz.ratio(possible_question, question)
                    if score > best_score:
                        best_match = question
                        best_score = score

                # Check if a match is found above a certain threshold
                if best_score >= 80:  # Adjust the threshold as needed
                    current_question = best_match
                    answer = question_answers[current_question].strip()
                    stored = True

                time.sleep(1)

            print(f'\nQuestion: "{current_question}"')
            print(f'Answer: "{answer}"')

            # Loop until the question is answered
            while not question_answered:

                # Store all buttons that can be potentially the one 
                buttons = driver.find_elements("xpath", "//button[contains(@data-functional-selector, 'answer-')]")

                # Iterate through each button
                for button in buttons:

                    # If the button's text matches the stored answer then click it 
                    if button.text.strip() == answer:
                        
                        try:
                            # Click on the button
                            button.click()

                            for i in range(20):
                                button.click()

                            print(f'-{button.text}-')

                        except Exception as e:
                            pass

                        # Set the condition to look for a question again
                        question_answered = True
                        
                        # Delete the question from the dictionary
                        del question_answers[current_question]
                        
                        print(f'Remaining answers: {len(question_answers)}')

        except Exception as e:
            pass  
