import sqlite3
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import threading


def get_database_connection(database_name):
    """
    Establish a connection to the database and create the table if it doesn't exist.
    """

    # Get the connection with the database
    connection = sqlite3.connect(database_name)

    # Get the cursor from the connection
    cursor = connection.cursor()

    # Attempt to create the database in case it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Questions (
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            UNIQUE(question, answer) -- Ensure no duplicate question -> answer 
        )
    ''')
    return connection


def store_kahoot_in_database(uuid, database_name='Kahoot.db'):
    """
    Fetch the details of a Kahoot game from the API and store the questions and answers in the database.
    """

    # Request api
    response = requests.get(f'https://play.kahoot.it/rest/kahoots/{uuid}')

    # Check if the response was successful (Code 200)
    if response.status_code == 200:

        # Parse the JSON response
        json_data = response.json()

        # Store the data from the questions
        if 'questions' in json_data:

            questions = json_data['questions']

            # Establish database connection
            with get_database_connection(database_name) as conn:
                
                # Get cursor from the connection
                cursor = conn.cursor()

                # Store how many insertions have been made
                inserted_count = 0  

                # Iterate through each question in the response
                for question in questions:

                    if 'choices' in question and 'question' in question:

                        question_text = question['question']

                        for choice in question['choices']:

                            if choice.get('correct'):

                                try:

                                    # Insert into the database
                                    cursor.execute(
                                        'INSERT INTO Questions (question, answer) VALUES (?, ?)',
                                        (question_text, choice['answer'])
                                    )
                                    inserted_count += 1

                                except sqlite3.IntegrityError:

                                    print(f"Duplicate entry skipped for question: {question_text} -> {choice['answer']}")

                # Commit changes
                conn.commit()

                print(f"Inserted {inserted_count} new questions into the database")
        else:
            print("No questions found in the quiz data.")
    else:
        print(f"Error getting api response, status code: {response.status_code}")


def get_uuids_from_profile(profile_url, timeout=30, class_name='kahoots-grid__KahootGrid-sc-x6x3n7-1', load_button_class_name='button__Button-sc-c6mvr2-0'):
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

        PREFIX = 'https://create.kahoot.it/details/'

        # Iterate over each element
        for element in elements:

            # Find all <a> elements within the current element
            links = element.find_elements(By.TAG_NAME, 'a')
            
            # Iterate over all <a> elements and extract their href attribute 
            for link in links:

                url = link.get_attribute('href')

                if PREFIX in url:
                    print(url)
                    urls.append(url.replace(PREFIX, ''))

    except Exception as e:
        print(e)

    finally:

        # Close the driver after the operation is done
        driver.quit()

        # Convert to a set to remove duplicated urls
        return list(set(urls))


if __name__ == '__main__':

    with open('Profile.txt', 'r', encoding='UTF-8') as f:
        url = f.read()

        if url:

            uuids = get_uuids_from_profile(url)
            print(f"Extracted UUIDs: {len(uuids)}")

            for uuid in uuids:

                threading.Thread(target=store_kahoot_in_database, args=(uuid,)).start()
        
        else:
            print('Invalid profile url in "Profile.txt"')
