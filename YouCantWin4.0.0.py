"""



▄██   ▄    ▄██████▄  ███    █▄   ▄████████    ▄████████ ███▄▄▄▄       ███      ▄█     █▄   ▄█  ███▄▄▄▄   
███   ██▄ ███    ███ ███    ███ ███    ███   ███    ███ ███▀▀▀██▄ ▀█████████▄ ███     ███ ███  ███▀▀▀██▄ 
███▄▄▄███ ███    ███ ███    ███ ███    █▀    ███    ███ ███   ███    ▀███▀▀██ ███     ███ ███▌ ███   ███ 
▀▀▀▀▀▀███ ███    ███ ███    ███ ███          ███    ███ ███   ███     ███   ▀ ███     ███ ███▌ ███   ███ 
▄██   ███ ███    ███ ███    ███ ███        ▀███████████ ███   ███     ███     ███     ███ ███▌ ███   ███ 
███   ███ ███    ███ ███    ███ ███    █▄    ███    ███ ███   ███     ███     ███     ███ ███  ███   ███ 
███   ███ ███    ███ ███    ███ ███    ███   ███    ███ ███   ███     ███     ███ ▄█▄ ███ ███  ███   ███ 
 ▀█████▀   ▀██████▀  ████████▀  ████████▀    ███    █▀   ▀█   █▀     ▄████▀    ▀███▀███▀  █▀    ▀█   █▀  
                                                                                                         



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
        
                            3.1.0
        Normalized text, removed unwanted characters, spanish tildes, html tags...
        that caused questions to not be recognized

                            4.0.0
        SQLite integration, individual question -> answer stored in a local database
        so there's no need to input the uuid beforehand if you already have your 
        teacher's profile id to scrape the latest kahoot's questions




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

-Circumvent randomized question / answer positions by performing OCR or getting html code (pls no, I dont wanna have to scan for question then locate answers zzzz :c) (fixed ver: 3.0.1) (Ocr pft, what was I on about)

-Get the kahoot id by just entering the game id (probably not possible, unless scanning for packages or something) (Sorta fixed ver 4.0.0 (13/12/2024))


==== WIP ====

Bake a cake

"""


from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException
from selenium.webdriver.common.by import By

import unicodedata
import sqlite3
import time


def remove_unwanted_tags(text):
    """ Remove unwanted tags and extra spaces given a text """

    # things to remove
    # SPACES MUST BE AT THE END, FIRST REMOVE UNWANTED TAGS, THEN NORMALIZE SPACING BETWEEN WORDS
    unwanted_data = ['&nbsp;', '&lt', '&gt', '<b>', '</b>', '<i>', '</i>', ' ', '  ', '   ', '    ', '     ', '      ', '       ', '        ']
    
    # Iterate through each 'thing' in the unwanted_data list
    for thing in unwanted_data:

        # Replace it with an empty space
        text = text.replace(thing, ' ')

    return text


def normalize_text(text):
    """Remove unwanted spaces and characters given a text"""

    # Normalize to NFD (decomposing characters with accents)
    text = unicodedata.normalize('NFD', text)
    
    # Remove combining characters (accents, tildes)
    text = ''.join(char for char in text if not unicodedata.combining(char))
    
    text = remove_unwanted_tags(text)

    # Lowercase and strip whitespace
    return text.strip().lower()


def get_questions_from_database(database_name='Kahoot.db'):
    """Get all of the questions and answers stored in the database"""
    with sqlite3.connect(database_name) as connection:

        # Get a cursor from the connection to execute queries
        cursor = connection.cursor()

        # Execute the query to select all questions and answers
        cursor.execute('''SELECT * FROM Questions''')

        # Fetch all results
        rows = cursor.fetchall()

        # Dictionary that will hold all of the questions -> answers
        questions = {}

        # Iterate over rows to create the dictionary
        for row in rows:

            # Store the question temporarily with normalised text
            question = normalize_text(row[0])
            answer = normalize_text(row[1])

            # Asign it to the dictionary
            questions[question] = answer  

        return questions




if __name__ == '__main__':

    # Get the data form the database
    my_dictionary = get_questions_from_database()

    if my_dictionary:
        print(f"Data stored correctly")
        print(f"Questions in the dictionary: {len(my_dictionary)}")
    else:
        print("NO DATA FOUND IN THE DATABASE")

    game_pin = input("Game Pin > ")
            
    driver = webdriver.Firefox()

    full_url = 'https://kahoot.it/?pin=' + game_pin + '&refer_method=link'

    driver.get(full_url)

    driver.set_window_size(600, 500)

    question = None # Store the current question
    answers = []    # Store the answers

    QUESTION_BEFORE_ANSWERS_CLASS_NAME = 'block-title__Title-sc-1kt4e1p-0'                  # Class name for the question that appears BEFORE the answers are shown
    QUESTION_WHILE_ANSWERS_CLASS_NAME = 'extensive-question-title__Title-sc-1m88qtl-0'      # Class name for the question that appears WHILE  the answers are shown (Backup in case of joining late or something)

    ANSWER_CLASS_NAME = 'choice__Choice-sc-ym3b8f-4'

    try:

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
                        # There's nothing that needs to be done, just ignore it
                        continue
                
                except KeyError as e:
                    print(f'Question {e} not found in the dictionary')
                    time.sleep(1)
                    
                question = None

    except NoSuchWindowException:
        print(f"Browser closed")

    except Exception as e:

        print(f"Something went wrong: {e}")