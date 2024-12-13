# YouCantWin

YouCantWin is my first serious Python program to automatically play Kahoot in class.

It started as a simple script that would print answers so you know ahead of time what option to click and never lose on your kahoots, 
but now its fully automated and designed to play any of the latest kahoots from your teacher since all of the questions and answers will be stored locally

1. **The kahoot must be public** otherwise you won't be able to retreive the questions and answers ahead of time <br><br>
2. If you frequently play kahoots from the same profile (your teacher's profile) you can store the profile ID to know where to look for the IDs

## How to set it up
1. Create a file called ```Profile.txt``` where you will place the id of the profile you want to scrap all ids for later use
2. Run ```Update Kahoot DataBase.py``` to scrape the latest kahoot's data and store it in your local database
3. You have successfully Added the latest 24 kahoot's from the profile you entered, you can run ```YouCantWin4.0.0.py``` and when it finds a match within the db it will click on the answer
