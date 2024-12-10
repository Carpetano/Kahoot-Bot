from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import requests
import unicodedata


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


def get_kahoot_urls(profile_url, timeout=30, class_name='kahoots-grid__KahootGrid-sc-x6x3n7-1', load_button_class_name='button__Button-sc-c6mvr2-0'):
    """Get the latest public kahoot urls from a kahoot profile"""

    # List where the urls will be stored
    urls = []

    # Initialize the Firefox WebDriver
    driver = webdriver.Firefox()

    # Open the profile
    driver.get(profile_url)

    try:

        # Wait until the element with class name provided is visible, or until timeout
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, class_name))
        )

        # Wait an extra second, just in case
        time.sleep(1)

        # Find the elements containing the Kahoot grid
        elements = driver.find_elements(By.CLASS_NAME, class_name)

        # Iterate over each element
        for element in elements:

            # Find all <a> elements within the current element
            links = element.find_elements(By.TAG_NAME, 'a')
            
            # Iterate over all <a> elements and extract their href attribute 
            for link in links:

                url = link.get_attribute('href')

                if url and url not in urls:
                    print(url)
                    urls.append(url)

    finally:
        # Close the driver after the operation is done
        driver.quit()

        # Convert to a set to remove duplicated urls
        return set(urls)


def urls_to_uuids(urls):
    """Convert from url to uuid"""
    uuids = []
    for url in urls:
        uuids.append(url.split('/')[-1])
        print(url)
    return uuids


def get_latest_kahoots_dictionary(uuids, delay_between_requests=0.5):
    # Store ALL of the questions and answers
    questions = {}

    print(f"\nNumber of Kahoots: {len(uuids)}")

    # Iterate through each uuid
    for index, uuid in enumerate(uuids):

        time.sleep(delay_between_requests)

        print(f"Requesting {uuid}")
        print(f"Remaining: {len(uuids) - index}")

        # Get the dictionary of the kahoot's uuid
        temp_dictionary = get_answers_dictionary(uuid)

        # Check if the dictionary returned is not None
        if temp_dictionary is not None:
            # Iterate through each entry in the dictionary
            for question, answer in temp_dictionary.items():
                # Add the question-answer pair to the questions dictionary
                questions[question] = answer
        else:
            print(f"Skipping UUID {uuid} due to failed API response.")

    return questions


def get_latest_kahoots_answers_from_profile(profile_url):

    urls = get_kahoot_urls(profile_url)

    uuids = urls_to_uuids(urls)

    long_dict = get_latest_kahoots_dictionary(uuids)

    return long_dict


def remove_unwanted_tags(text):
    return text.replace('&nbsp;', ' ').replace('&lt', ' ').replace('&gt', ' ').replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '').replace('  ', ' ').replace('   ', ' ').replace('     '. ' ')
    


with open('Profile.txt', 'r', encoding='UTF-8') as f:
    profile_url = f.read().strip()

if not profile_url:
    print('No profile found in "Profile.txt"')
    
print(f"Scanning: {profile_url}")


all_questions = get_latest_kahoots_answers_from_profile(profile_url)


with open('LatestKahootsQuestions.txt', 'w', encoding='UTF-8') as f:

    print('Writing to file...')

    for q, a in all_questions.items():

        line = f"{remove_unwanted_tags(q)} -|@|- {remove_unwanted_tags(a)}"

        line = normalize_text(line)

        f.write(f"{line}\n")

print('Done')